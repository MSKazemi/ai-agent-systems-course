"""
LLM Configuration — Azure OpenAI and Gemini provider switch

This module handles LLM provider selection and Azure credential mapping.
All agents (coordinator, remote math, remote prime) use get_llm_model().

ENV VARS:
    LLM_PROVIDER     : "azure" | "gemini" (default: auto based on what's configured)
    AZURE_OPENAI_*   : For Azure (see .env.example)
    GOOGLE_API_KEY   : For Gemini

AZURE MAPPING:
    KubeIntellect uses AZURE_OPENAI_*, but LiteLLM expects AZURE_API_*.
    _normalize_azure_env() copies values so both conventions work.
"""

import os
from typing import Any


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
        - LLM_PROVIDER=azure   → Azure OpenAI via LiteLLM (requires Azure env vars)
        - LLM_PROVIDER=gemini  → "gemini-2.0-flash" (requires GOOGLE_API_KEY)
        - Unset                → Azure if configured, else Gemini

    Returns:
        Either LiteLlm(model="azure/gpt-4o") or "gemini-2.0-flash"
    """
    provider = (os.getenv("LLM_PROVIDER") or "").lower().strip()
    use_azure = is_azure_configured()

    if provider == "azure":
        if not use_azure:
            raise RuntimeError(
                "LLM_PROVIDER=azure but Azure not configured. "
                "Set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT in .env"
            )
        from google.adk.models.lite_llm import LiteLlm
        return LiteLlm(model=f"azure/{get_azure_deployment()}")

    if provider == "gemini":
        return "gemini-2.0-flash"

    # Auto-select
    if use_azure:
        from google.adk.models.lite_llm import LiteLlm
        return LiteLlm(model=f"azure/{get_azure_deployment()}")
    return "gemini-2.0-flash"
