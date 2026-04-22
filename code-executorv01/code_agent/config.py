"""
Configuration for the code-execution agent.
All values can be overridden via a .env file in this directory.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

# --- Paths ---
DATA_DIR = BASE_DIR / "data"
PLOTS_DIR = BASE_DIR / "plots"
DEFAULT_DATA_FILE = DATA_DIR / "device_data.csv"

DATA_DIR.mkdir(parents=True, exist_ok=True)
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# --- Ollama connection ---
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.6:35b-a3b")

# 'native' -> models with built-in function calling (llama3.1, qwen2.5, ...)
# 'tagged' -> models that output <tool_call>...</tool_call> text tags
TOOL_CALL_MODE = os.getenv("TOOL_CALL_MODE", "native").strip().lower()
if TOOL_CALL_MODE not in ("native", "tagged"):
    TOOL_CALL_MODE = "native"

# --- Model parameters ---
N_CTX = int(os.getenv("OLLAMA_NUM_CTX", "32768"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "8192"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
TOP_P = float(os.getenv("TOP_P", "0.8"))
TOP_K = int(os.getenv("TOP_K", "40"))
MIN_P = float(os.getenv("MIN_P", "0.00"))
REPEAT_PENALTY = float(os.getenv("REPEAT_PENALTY", "1.0"))

# --- Agent limits ---
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "8"))
MAX_MESSAGES = int(os.getenv("MAX_MESSAGES", "30"))

timeout_str = os.getenv("CODE_EXECUTION_TIMEOUT", "60")
CODE_EXECUTION_TIMEOUT: int | None = (
    int(timeout_str) if timeout_str and timeout_str.lower() != "none" else None
)
