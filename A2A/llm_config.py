"""
LLM Configuration — Ollama (default), Azure OpenAI, and Gemini provider switch.

All agents (coordinator, remote math, remote prime) use get_llm_model().
Reads .env from the current directory or any parent (finds root .env automatically).

ENV VARS (set in root .env or A2A/.env):
    LLM_PROVIDER     : "ollama" | "azure" | "gemini" (default: ollama)
    OLLAMA_MODEL     : model name (default: qwen3.5:35b)
    OLLAMA_BASE_URL  : Ollama endpoint (default: http://localhost:11434)
    AZURE_OPENAI_*   : For Azure (see .env.example)
    GOOGLE_API_KEY   : For Gemini

AZURE MAPPING:
    LiteLLM expects AZURE_API_*, but we also support AZURE_OPENAI_*.
    _normalize_azure_env() copies values so both conventions work.
"""

import os
from typing import Any
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def _normalize_azure_env() -> None:
    """
    Map KubeIntellect-style Azure env vars to LiteLLM format.

    LiteLLM reads: AZURE_API_KEY, AZURE_API_BASE, AZURE_API_VERSION
    We support:    AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION

    Only copies if the LiteLLM var is not already set.
    """
    if os.getenv("AZURE_OPENAI_API_KEY") and not os.getenv("AZURE_API_KEY"):
        os.environ["AZURE_API_KEY"] = os.environ["AZURE_OPENAI_API_KEY"]
    if os.getenv("AZURE_OPENAI_ENDPOINT") and not os.getenv("AZURE_API_BASE"):
        base = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
        os.environ["AZURE_API_BASE"] = base
    if os.getenv("AZURE_OPENAI_API_VERSION") and not os.getenv("AZURE_API_VERSION"):
        os.environ["AZURE_API_VERSION"] = os.environ["AZURE_OPENAI_API_VERSION"]


def get_azure_deployment() -> str:
    """
    Return the Azure OpenAI deployment name for chat completions.

    Used when building the LiteLLM model string: azure/<deployment>
    """
    return os.getenv("AZURE_PRIMARY_LLM_DEPLOYMENT_NAME", "gpt-4o")


def is_azure_configured() -> bool:
    """
    Check if Azure credentials are available (after normalizing env vars).
    """
    _normalize_azure_env()
    return bool(os.getenv("AZURE_API_KEY") and os.getenv("AZURE_API_BASE"))


def get_llm_model() -> Any:
    """
    Return the LLM model object/string for ADK Agent.

    Selection logic:
        - LLM_PROVIDER=ollama  → local Ollama via LiteLLM (default, no key needed)
        - LLM_PROVIDER=azure   → Azure OpenAI via LiteLLM (requires Azure env vars)
        - LLM_PROVIDER=gemini  → "gemini-2.0-flash" (requires GOOGLE_API_KEY)
        - Unset                → defaults to ollama

    Returns:
        LiteLlm instance or "gemini-2.0-flash" string
    """
    provider = (os.getenv("LLM_PROVIDER") or "ollama").lower().strip()

    if provider == "ollama":
        from google.adk.models.lite_llm import LiteLlm
        model = os.getenv("OLLAMA_MODEL", "qwen3.5:35b")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return LiteLlm(
            model=f"ollama_chat/{model}",
            api_base=base_url,
            stream=False,
        )

    if provider == "azure":
        if not is_azure_configured():
            raise RuntimeError(
                "LLM_PROVIDER=azure but Azure not configured. "
                "Set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT in .env"
            )
        from google.adk.models.lite_llm import LiteLlm
        return LiteLlm(model=f"azure/{get_azure_deployment()}")

    if provider == "gemini":
        return "gemini-2.0-flash"

    raise ValueError(
        f"Unknown LLM_PROVIDER='{provider}'. Choose: ollama, azure, gemini"
    )
