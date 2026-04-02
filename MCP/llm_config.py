"""
LLM Configuration for MCP demos — OpenAI-compatible client.

Supports Ollama (local), Azure OpenAI, and Gemini via OpenAI-compatible API.
Mirror of A2A/llm_config.py but returns an openai client instead of an ADK model,
since MCP demos don't use Google ADK.

ENV VARS:
    LLM_PROVIDER                    : "ollama" | "azure" | "gemini" (default: ollama)
    OLLAMA_MODEL                    : model name (default: qwen3.5:35b)
    OLLAMA_BASE_URL                 : Ollama endpoint (default: http://localhost:11434)
    AZURE_OPENAI_API_KEY            : Azure API key
    AZURE_OPENAI_ENDPOINT           : Azure endpoint URL
    AZURE_OPENAI_API_VERSION        : Azure API version (default: 2024-02-01)
    AZURE_PRIMARY_LLM_DEPLOYMENT_NAME : Azure deployment name (default: gpt-4o)
    GOOGLE_API_KEY                  : Gemini API key
    GEMINI_MODEL                    : Gemini model (default: gemini-2.0-flash)
"""

import os


def get_openai_client():
    """
    Return (client, model_name) for the configured LLM provider.

    All three providers expose an OpenAI-compatible REST API, so we use the
    openai Python package for all of them — only the base_url and api_key differ.

    Returns:
        Tuple of (openai.OpenAI client, model name string)
    """
    from openai import OpenAI

    provider = (os.getenv("LLM_PROVIDER") or "ollama").lower().strip()

    if provider == "azure":
        from openai import AzureOpenAI
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
        )
        model = os.getenv("AZURE_PRIMARY_LLM_DEPLOYMENT_NAME", "gpt-4o")
        return client, model

    if provider == "gemini":
        client = OpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=os.getenv("GOOGLE_API_KEY"),
        )
        model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        return client, model

    # Default: ollama
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/") + "/v1"
    model = os.getenv("OLLAMA_MODEL", "qwen3.5:35b")
    client = OpenAI(base_url=base_url, api_key="ollama")
    return client, model
