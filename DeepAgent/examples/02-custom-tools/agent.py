"""
Example 02 — Custom Tools

Shows how to add your own Python functions as tools.

Key points:
  - Use @tool decorator from langchain_core.tools
  - The docstring becomes the tool description the LLM reads
  - Pass your tools as a list to create_deep_agent(tools=[...])
  - Your tools are added alongside the built-in ones

Run:
  cd DeepAgent
  source .venv/bin/activate
  python examples/02-custom-tools/agent.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dotenv import load_dotenv
from langchain_core.tools import tool
from deepagents import create_deep_agent
from llm_config import get_llm_model

load_dotenv()


# --- Define custom tools ---

@tool
def get_city_population(city: str) -> str:
    """
    Return the approximate population of a city.
    Use this when the user asks about population figures.
    """
    # Hardcoded for demo purposes.
    populations = {
        "tokyo": "13.96 million",
        "new york": "8.34 million",
        "london": "8.98 million",
        "paris": "2.16 million",
        "berlin": "3.67 million",
    }
    key = city.lower().strip()
    if key in populations:
        return f"{city.title()} population: {populations[key]}"
    return f"Population data for '{city}' is not available in this demo."


@tool
def celsius_to_fahrenheit(celsius: float) -> str:
    """
    Convert a temperature from Celsius to Fahrenheit.
    Use this when the user asks to convert temperature.
    """
    fahrenheit = (celsius * 9 / 5) + 32
    return f"{celsius}°C = {fahrenheit:.1f}°F"


def main():
    llm = get_llm_model()

    # Register custom tools alongside the built-in ones
    agent = create_deep_agent(
        model=llm,
        tools=[get_city_population, celsius_to_fahrenheit],
        system_prompt=(
            "You are a helpful assistant with access to city population data "
            "and temperature conversion tools. Use them when relevant."
        ),
    )

    # Ask a question that requires both custom tools
    task = (
        "What is the population of Tokyo? "
        "Also, Tokyo's average summer temperature is 30°C — what is that in Fahrenheit?"
    )

    print("Task:", task)
    print("-" * 60)

    result = agent.invoke({
        "messages": [{"role": "user", "content": task}]
    })

    final_message = result["messages"][-1]
    print("\nAgent response:")
    print(final_message.content)

    # Show the tool calls that were made
    print("\n--- Tool calls made ---")
    for msg in result["messages"]:
        # AIMessage with tool_calls shows what the LLM decided to call
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"  Called: {tc['name']}({tc['args']})")


if __name__ == "__main__":
    main()
