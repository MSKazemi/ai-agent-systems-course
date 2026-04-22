"""
Tool definitions for the code-execution agent.

Provides one tool: execute_python — runs LLM-generated code in an isolated
subprocess with a timeout, then returns structured output the graph can route on.

Also provides load_data: loads a CSV into the REPL as the 'df' variable and
returns metadata the agent uses to understand the dataset.
"""

import os
import sys
import io
import json
import builtins
from queue import Empty
from typing import Dict, Any

import multiprocessing as mp
from multiprocessing.queues import Queue as MPQueue

from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL

from config import DEFAULT_DATA_FILE, CODE_EXECUTION_TIMEOUT, PLOTS_DIR

import matplotlib
matplotlib.use("Agg")  # non-interactive backend — saves to file, no display needed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


# Output size limits — keep the LLM context window manageable
MAX_OUTPUT_SAFETY = 10_000   # hard truncate at 10 KB to prevent crashes
MAX_OUTPUT_TO_LLM = 2_000   # only show 2 KB to the LLM

# Shared persistent REPL — variables survive between tool calls in stateful mode
_repl: PythonREPL = PythonREPL(_locals={})

# Track the active dataset path so the subprocess can reload it
_ACTIVE_DATA_PATH: str = str(DEFAULT_DATA_FILE)

# Inject common libraries into builtins so generated code can use them without importing
builtins.pd = pd
builtins.np = np
builtins.plt = plt
builtins.os = os
builtins.sys = sys
builtins.io = io
builtins.stats = stats


# ---------------------------------------------------------------------------
# Subprocess isolation
# ---------------------------------------------------------------------------

def _get_mp_context() -> mp.context.BaseContext:
    # forkserver/spawn avoids "fork-from-thread" issues on Linux
    try:
        return mp.get_context("forkserver")
    except ValueError:
        return mp.get_context("spawn")


def _subprocess_target(queue: MPQueue, code: str, data_path: str) -> None:
    """
    Runs inside the subprocess.

    Re-injects all builtins and reloads 'df' from scratch on every call —
    the subprocess doesn't inherit the parent's memory, so we must do this.
    """
    try:
        _repl.locals.update({
            "pd": pd, "np": np, "plt": plt,
            "os": os, "sys": sys, "io": io, "stats": stats,
        })

        # Reload the dataset
        df = pd.read_csv(data_path or str(DEFAULT_DATA_FILE))
        for col in df.columns:
            if any(k in col.lower() for k in ["date", "time", "timestamp"]):
                try:
                    df[col] = pd.to_datetime(df[col], errors="coerce")
                except Exception:
                    pass
        df = df.dropna(axis=1, how="all")
        _repl.locals["df"] = df

        result = _repl.run(code)
        queue.put({"status": "success", "result": result or ""})

    except Exception as e:
        queue.put({
            "status": "error",
            "error_type": type(e).__name__,
            "error_message": str(e),
        })


def _run_in_subprocess(code: str, timeout: int, data_path: str) -> str:
    """Run code in an isolated subprocess and return its stdout."""
    ctx = _get_mp_context()
    queue = ctx.Queue()
    process = ctx.Process(target=_subprocess_target, args=(queue, code, data_path))
    process.start()
    process.join(timeout=timeout)

    if process.is_alive():
        process.terminate()
        process.join(timeout=2)
        if process.is_alive():
            process.kill()
            process.join()
        try:
            queue.close()
            queue.join_thread()
        except Exception:
            pass
        raise TimeoutError(f"Code execution exceeded {timeout}s timeout")

    try:
        response = queue.get(timeout=2)
    except Empty:
        raise RuntimeError(f"Subprocess crashed (exit code {process.exitcode})")
    finally:
        try:
            queue.close()
            queue.join_thread()
        except Exception:
            pass

    if response["status"] == "success":
        return response["result"]
    raise RuntimeError(f"{response['error_type']}: {response['error_message']}")


# ---------------------------------------------------------------------------
# Output classification helpers
# ---------------------------------------------------------------------------

DEFINITE_ERRORS = [
    "Traceback", "Error:", "Exception:", "NameError", "ValueError",
    "TypeError", "KeyError", "AttributeError", "IndexError",
    "FileNotFoundError", "ImportError", "SyntaxError",
]

KNOWN_WARNINGS = [
    "UserWarning", "RuntimeWarning", "FutureWarning",
    "SettingWithCopyWarning", "Python REPL can execute arbitrary code.",
]


def _snapshot_plots() -> Dict[str, float]:
    """Record current plot files so we can detect new ones after execution."""
    if not PLOTS_DIR.exists():
        return {}
    return {p.name: p.stat().st_mtime for p in PLOTS_DIR.glob("*.png") if p.is_file()}


def _new_plots(before: Dict[str, float], after: Dict[str, float]) -> list:
    return [str(PLOTS_DIR / name) for name in after if name not in before]


def _make_error_response(error_type: str, error_message: str, code: str, action: str) -> str:
    """Format a structured error response the graph can route on."""
    meta = json.dumps({"error_type": error_type, "error_message": error_message})
    return (
        f"[ERROR_META] {meta}\n\n"
        "[PYTHON_EXECUTION_FAILED]\n\n"
        f"**Error Type:** {error_type}\n\n"
        f"**Error Message:** {error_message}\n\n"
        f"**Your Code:**\n```\n{code}\n```\n\n"
        f"**Action Required:** {action}"
    )


# ---------------------------------------------------------------------------
# The tool
# ---------------------------------------------------------------------------

@tool
def execute_python(code: str) -> str:
    """Execute Python code in the persistent REPL and return structured output."""
    print(f"\n[TOOL] execute_python\n{code}\n", file=sys.stderr)

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    plots_before = _snapshot_plots()

    # Wrap the code so tracebacks go to stdout (visible to the LLM)
    wrapped = (
        "import sys, traceback\ntry:\n"
        + "\n".join("    " + line for line in code.splitlines())
        + "\nexcept Exception:\n    traceback.print_exc(file=sys.stdout)\n"
    )

    try:
        if CODE_EXECUTION_TIMEOUT:
            output = _run_in_subprocess(wrapped, CODE_EXECUTION_TIMEOUT, _ACTIVE_DATA_PATH)
        else:
            output = _repl.run(wrapped) or ""

        if len(output) > MAX_OUTPUT_SAFETY:
            output = output[:MAX_OUTPUT_SAFETY] + "\n... [TRUNCATED]"

    except TimeoutError:
        return _make_error_response(
            "TimeoutError",
            f"Code exceeded {CODE_EXECUTION_TIMEOUT}s — use vectorized operations or reduce data size.",
            code,
            "Rewrite with faster pandas/numpy operations.",
        )
    except Exception as e:
        return _make_error_response(type(e).__name__, str(e), code, "Fix the error and retry.")

    # Check for runtime errors in the output
    is_error = any(marker in output for marker in DEFINITE_ERRORS)

    if is_error:
        truncated = output[:2000] + "\n... [TRUNCATED]" if len(output) > 2000 else output
        return _make_error_response(
            "ExecutionError", output.strip().splitlines()[-1] if output.strip() else "Unknown error",
            code,
            f"Fix the error shown in the traceback:\n```\n{truncated}\n```",
        )

    # Success path
    display_output = output.strip()
    if len(display_output) > MAX_OUTPUT_TO_LLM:
        display_output = display_output[:MAX_OUTPUT_TO_LLM] + "\n... [TRUNCATED]"

    plots_after = _snapshot_plots()
    new_plot_files = _new_plots(plots_before, plots_after)

    # Enforce plot-saving protocol
    c = code.replace(" ", "")
    if "plt.show(" in c:
        return _make_error_response(
            "PlotProtocolViolation",
            "plt.show() is not allowed — save the plot instead.",
            code,
            "Replace plt.show() with: plt.savefig(str(PLOTS_DIR/'name.png'), dpi=300, bbox_inches='tight'); plt.close()",
        )

    uses_plt = any(m in c for m in ("plt.plot(", "plt.scatter(", "plt.hist(", "plt.bar(", ".plot("))
    if uses_plt and "plt.savefig(" not in c and not new_plot_files:
        return _make_error_response(
            "MissingPlotSave",
            "Plotting code detected but no PNG was saved.",
            code,
            "Add: plt.savefig(str(PLOTS_DIR/'name.png'), dpi=300, bbox_inches='tight'); plt.close()",
        )

    if not display_output and not new_plot_files:
        return _make_error_response(
            "NoObservableOutput",
            "Code ran but produced no output and no plots.",
            code,
            "Add print() statements to show results.",
        )

    return (
        "SUCCESS\n\n"
        f"**STDOUT:**\n---\n{display_output}\n---\n\n"
        f"**ARTIFACTS:**\n---\n{json.dumps({'plots': new_plot_files})}\n---"
    )


# Registry exposed to the LangGraph agent
tools: list = [execute_python]


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_data(data_path: str) -> Dict[str, Any] | None:
    """
    Load a CSV into the REPL as 'df'.

    Automatically:
    - Converts date/time columns to datetime
    - Drops all-NaN columns
    - Converts object columns to numeric when most values are numbers

    Returns metadata so the agent knows the shape and structure of the data.
    """
    global _ACTIVE_DATA_PATH

    try:
        df = pd.read_csv(data_path)
    except Exception as e:
        print(f"[ERROR] Cannot load {data_path}: {e}", file=sys.stderr)
        return None

    _ACTIVE_DATA_PATH = str(data_path)

    # Parse datetime columns
    for col in df.columns:
        if any(k in col.lower() for k in ["date", "time", "timestamp"]):
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except Exception:
                pass

    df = df.dropna(axis=1, how="all")

    # Promote object columns that are mostly numeric
    for col in df.select_dtypes(include=["object"]).columns:
        numeric = pd.to_numeric(df[col], errors="coerce")
        if numeric.notna().sum() / len(df) > 0.5:
            df[col] = numeric

    _repl.locals["df"] = df
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    # Build metadata for the LLM context
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    datetime_cols = df.select_dtypes(include=["datetime", "datetime64"]).columns

    numeric_stats = {}
    for col in numeric_cols:
        try:
            s = df[col].agg(["min", "max", "mean", "std"])
            numeric_stats[col] = {k: float(s[k]) for k in ["min", "max", "mean", "std"]}
        except Exception:
            pass

    datetime_info = {}
    potential_time_index = None
    for col in datetime_cols:
        col_data = df[col].dropna()
        if len(col_data) == 0:
            continue
        if col_data.is_unique and col_data.is_monotonic_increasing:
            potential_time_index = col
        diffs = col_data.diff().dropna()
        if len(diffs) > 0:
            median_s = diffs.median().total_seconds()
            datetime_info[col] = {
                "min": str(col_data.min()),
                "max": str(col_data.max()),
                "duration": str(col_data.max() - col_data.min()),
                "sampling_median_seconds": round(median_s, 2),
            }

    metadata = {
        "data_preview": df.head(5).to_string(),
        "rows": len(df),
        "columns": list(df.columns),
        "numeric_columns": numeric_stats,
        "datetime_columns": datetime_info,
        "potential_time_index": potential_time_index,
    }

    print(f"[DATA] Loaded {len(df)} rows × {len(df.columns)} cols into REPL.", file=sys.stderr)
    return metadata
