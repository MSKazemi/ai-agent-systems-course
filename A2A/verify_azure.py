#!/usr/bin/env python3
"""
Verify Azure OpenAI credentials work with LiteLLM.

Use this script to test your .env credentials before running the agents.
If you get 401 errors in the app, run this to isolate the issue.

RUN:
    python verify_azure.py

REQUIRES:
    - .env with AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT

EXIT CODES:
    0 = success (Azure responded)
    1 = failure (missing config or Azure error)
"""

import os
from dotenv import load_dotenv

load_dotenv()

from llm_config import get_azure_deployment, is_azure_configured

# Apply the same env var mapping used by agents (KubeIntellect → LiteLLM)
is_azure_configured()


def main() -> int:
    """
    Test Azure OpenAI by sending a minimal chat completion request.

    Returns:
        0 on success, 1 on failure.
    """
    key = os.getenv("AZURE_API_KEY", "")
    base = os.getenv("AZURE_API_BASE", "")
    deployment = get_azure_deployment()

    print("Config check:")
    print(f"  AZURE_API_BASE: {base or '(not set)'}")
    print(f"  AZURE_API_KEY: {'***' + key[-4:] if key else '(not set)'}")
    print(f"  Deployment: {deployment}")
    print()

    if not key or not base:
        print("ERROR: Set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT in .env")
        return 1

    try:
        import litellm
        resp = litellm.completion(
            model=f"azure/{deployment}",
            messages=[{"role": "user", "content": "Say 'OK' if you receive this."}],
        )
        print("SUCCESS:", resp.choices[0].message.content)
        return 0
    except Exception as e:
        print("FAILED:", e)
        return 1


if __name__ == "__main__":
    exit(main())
