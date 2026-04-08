"""
Shared LLM configuration — repo root.

Used by LangGraph examples (and any other module that needs a LangChain model).
DeepAgent, MCP, and A2A each have their own llm_config.py that mirrors this
interface for their specific LLM abstraction.

ENV VARS (set in root .env):
    LLM_PROVIDER        : ollama | azure | gemini | openai  (default: ollama)
    OLLAMA_MODEL        : model name          (default: qwen3.5:35b)
    OLLAMA_BASE_URL     : Ollama endpoint     (default: http://localhost:11434)
    AZURE_OPENAI_API_KEY
    AZURE_OPENAI_ENDPOINT
    AZURE_OPENAI_DEPLOYMENT                  (default: gpt-4o)
    AZURE_OPENAI_API_VERSION                 (default: 2024-02-01)
    GOOGLE_API_KEY
    OPENAI_API_KEY
"""

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_langchain_model():
    """Return a LangChain ChatModel for the configured provider."""
    provider = os.getenv("LLM_PROVIDER", "ollama").lower().strip()

    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "qwen3.5:35b"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        )

    if provider == "azure":
        from langchain_openai import AzureChatOpenAI
        return AzureChatOpenAI(
            azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
            temperature=0,
        )

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.environ["GOOGLE_API_KEY"],
            temperature=0,
        )

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-4o", temperature=0)

    raise ValueError(
        f"Unknown LLM_PROVIDER='{provider}'. "
        "Choose: ollama, azure, gemini, openai"
    )


# Alias used by DeepAgent-style imports
get_llm_model = get_langchain_model
