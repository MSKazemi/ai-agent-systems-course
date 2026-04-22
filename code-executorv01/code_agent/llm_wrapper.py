"""
OllamaEnforcingWrapper — Ollama LLM calls with protocol enforcement.

Two modes controlled by allow_text:

  allow_text=False (work loop):
    - The LLM MUST produce a tool call every turn.
    - Plain text replies → PROTOCOL_ERROR → graph retries the agent node.
    - Unresolved execution error + no tool call → enforcement message.

  allow_text=True (finalize):
    - The LLM MUST produce plain text only.
    - Tool calls here → PROTOCOL_ERROR → graph retries finalize.

This enforcement layer means the graph's routing logic can always trust the
output shape without depending on prompt engineering alone.
"""

import sys
import re
import json
from typing import List, Optional, Tuple, Dict, Any

from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, ToolMessage

from config import (
    TEMPERATURE, TOP_P, TOP_K, MIN_P, REPEAT_PENALTY,
    MAX_TOKENS, N_CTX, OLLAMA_HOST, OLLAMA_MODEL, TOOL_CALL_MODE,
)


class OllamaEnforcingWrapper:
    def __init__(self, tools: list):
        self._model = ChatOllama(
            base_url=OLLAMA_HOST,
            model=OLLAMA_MODEL,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            top_k=TOP_K,
            min_p=MIN_P,
            repeat_penalty=REPEAT_PENALTY,
            num_predict=MAX_TOKENS,
            num_ctx=N_CTX,
        )
        # In native mode, bind tools so the model knows their schema
        self._model_with_tools = (
            self._model.bind_tools(tools) if TOOL_CALL_MODE == "native" else self._model
        )
        print(f"[LLM] {OLLAMA_MODEL} @ {OLLAMA_HOST} | mode={TOOL_CALL_MODE}", file=sys.stderr)

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def invoke(self, messages: List, *, allow_text: bool = False) -> AIMessage:
        """
        Call the LLM and enforce the protocol contract on the response.
        Returns an AIMessage with metadata.parse_status set to one of:
          "SUCCESS"        — valid response
          "OK"             — plain text in finalize (allowed)
          "PROTOCOL_ERROR" — violation, graph should retry
          "FALLBACK"       — deterministic fallback
        """
        print(f"[LLM] invoking | msgs={len(messages)} allow_text={allow_text}", file=sys.stderr)

        try:
            response: AIMessage = self._model_with_tools.invoke(messages)
        except Exception as e:
            return self._protocol_error(
                f"[LLM_TRANSPORT_ERROR] {type(e).__name__}: {e}",
                reason="transport_error",
                allow_text=allow_text,
            )

        content = response.content or ""
        tool_calls = getattr(response, "tool_calls", []) or []

        # --- Tagged mode: parse <tool_call>...</tool_call> from raw text ---
        if TOOL_CALL_MODE == "tagged":
            parsed_calls, clean_text, parse_error = self._parse_tagged(content)

            if parse_error:
                return self._protocol_error(
                    f"[FORMATTING_ERROR] {parse_error}\nOutput a single <tool_call>{{...}}</tool_call>.",
                    reason="tagged_parse_failed",
                    allow_text=allow_text,
                )

            if parsed_calls:
                msg = AIMessage(content=clean_text, tool_calls=parsed_calls)
                msg.metadata = {"parse_status": "SUCCESS", "allow_text": bool(allow_text)}
                response, tool_calls = msg, parsed_calls
            else:
                response = self._make_msg(clean_text, "OK" if allow_text else "NOTOOLCALL",
                                          allow_text=allow_text)
                tool_calls = []

        # --- Finalize enforcement: tool calls are FORBIDDEN ---
        if allow_text and tool_calls:
            print("[LLM] Finalize: tool call found (forbidden) → retry", file=sys.stderr)
            return self._protocol_error(
                "[FINALIZE_ENFORCEMENT] Return plain text only — no tool calls.",
                reason="tool_call_in_finalize",
                allow_text=True,
            )

        # --- Work-loop enforcement: tool call is REQUIRED ---
        had_unresolved_error = self._has_unresolved_error(messages)
        if had_unresolved_error and not tool_calls:
            print("[LLM] Unresolved error, no tool call → enforcement", file=sys.stderr)
            return self._protocol_error(
                "[LLM_PROTOCOL_ENFORCEMENT] There is an unresolved execution error.\n"
                "Output exactly ONE execute_python tool call with corrected code.",
                reason="unresolved_error_no_tool_call",
                allow_text=allow_text,
            )

        if tool_calls:
            response.metadata = getattr(response, "metadata", {}) or {}
            response.metadata.update({"parse_status": "SUCCESS", "allow_text": bool(allow_text)})
            return response

        if not allow_text:
            print("[LLM] Missing tool call → enforcement", file=sys.stderr)
            return self._protocol_error(
                "[LLM_PROTOCOL_ENFORCEMENT] You must call execute_python. Output a tool call only.",
                reason="missing_tool_call",
                allow_text=allow_text,
            )

        # Finalize, plain text — all good
        response.metadata = getattr(response, "metadata", {}) or {}
        response.metadata.update({"parse_status": "OK", "allow_text": True})
        return response

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    @staticmethod
    def _make_msg(content: str, parse_status: str, *, allow_text: bool, **kw) -> AIMessage:
        msg = AIMessage(content=content or "")
        msg.metadata = {"parse_status": parse_status, "allow_text": bool(allow_text), **kw}
        return msg

    def _protocol_error(self, content: str, *, reason: str, allow_text: bool) -> AIMessage:
        return self._make_msg(
            content, "PROTOCOL_ERROR", allow_text=allow_text, reason=reason, retryable=True
        )

    @staticmethod
    def _has_unresolved_error(messages: List) -> bool:
        """True if the last ToolMessage reports an execution failure."""
        for m in reversed(messages):
            if isinstance(m, ToolMessage):
                up = (m.content or "").upper()
                if "[PYTHON_EXECUTION_FAILED]" in up:
                    return True
                if "SUCCESS" in up:
                    return False
        return False

    # -----------------------------------------------------------------------
    # Tagged tool-call parsing
    # -----------------------------------------------------------------------

    @classmethod
    def _parse_tagged(cls, text: str) -> Tuple[Optional[list], str, Optional[str]]:
        """
        Extract a <tool_call>{...}</tool_call> block from raw model text.
        Returns (tool_calls, clean_text, error_reason).
        """
        if not text:
            return None, "", None

        has_open = "<tool_call>" in text
        has_close = "</tool_call>" in text
        if has_open != has_close:
            return None, cls._strip_tags(text), "mismatched_tool_call_tags"

        blocks = re.findall(r"<tool_call>(.*?)</tool_call>", text, flags=re.DOTALL | re.IGNORECASE)
        clean = cls._strip_tags(text)

        if not blocks:
            return None, clean, None
        if len(blocks) > 1:
            return None, clean, f"multiple_tool_calls({len(blocks)})"

        payload, err = cls._parse_json(blocks[0].strip())
        if payload is None:
            return None, clean, err

        tool_calls, err2 = cls._build_tool_calls(payload)
        return tool_calls, clean, err2

    @staticmethod
    def _strip_tags(text: str) -> str:
        return re.sub(r"<tool_call>.*?</tool_call>", "", text, flags=re.DOTALL | re.IGNORECASE).strip()

    @staticmethod
    def _parse_json(inner: str) -> Tuple[Optional[dict], Optional[str]]:
        try:
            return json.loads(inner), None
        except Exception as e:
            first_err = str(e)
        try:
            from json_repair import repair_json
            repaired = repair_json(inner)
            return json.loads(repaired), None
        except Exception as e2:
            return None, f"json_parse_failed: {first_err}"

    @staticmethod
    def _build_tool_calls(payload: Dict[str, Any]) -> Tuple[Optional[list], Optional[str]]:
        name = payload.get("name")
        args = payload.get("arguments") or payload.get("args") or payload.get("parameters")
        if name != "execute_python":
            return None, f"unexpected_tool_name: {name}"
        if not isinstance(args, dict):
            return None, "arguments_not_object"
        code = args.get("code")
        if not isinstance(code, str) or not code.strip():
            return None, "missing_or_empty_code"
        return [{"name": "execute_python", "args": {"code": code}, "id": "tagged-1"}], None
