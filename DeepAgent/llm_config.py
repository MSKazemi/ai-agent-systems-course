"""
LLM provider selection for DeepAgent examples.

Set LLM_PROVIDER in your .env file:
  LLM_PROVIDER=openai   → requires OPENAI_API_KEY
  LLM_PROVIDER=azure    → requires AZURE_OPENAI_* vars
  LLM_PROVIDER=gemini   → requires GOOGLE_API_KEY
  LLM_PROVIDER=ollama   → requires OLLAMA_MODEL + OLLAMA_BASE_URL

Returns a LangChain chat model compatible with DeepAgent's create_deep_agent().
"""

import os
from dotenv import load_dotenv

load_dotenv()


def get_llm_model():
    """Return a LangChain chat model based on LLM_PROVIDER env var."""
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="gpt-4o", temperature=0)

    elif provider == "azure":
        from langchain_openai import AzureChatOpenAI
        return AzureChatOpenAI(
            azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version="2024-02-01",
            temperature=0,
        )

    elif provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=os.environ["GOOGLE_API_KEY"],
            temperature=0,
        )

    elif provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        )

    else:
        raise ValueError(
            f"Unknown LLM_PROVIDER='{provider}'. "
            "Choose: openai, azure, gemini, ollama"
        )
