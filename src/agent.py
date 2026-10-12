"""
Stock Reorder Assistant - conversational agent.

Uses Groq (Llama 3.3 70B) with tool calling to answer
business questions about inventory in natural language.
"""

import json
import os

from dotenv import load_dotenv
from groq import Groq

from agent_tools import TOOLS

load_dotenv()


def _get_groq_key():
    """Read GROQ_API_KEY from .env locally, or Streamlit secrets in the cloud."""
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        raise RuntimeError("GROQ_API_KEY not found in .env or Streamlit secrets")


client = Groq(api_key=_get_groq_key())
MODEL = "openai/gpt-oss-120b"

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "list_products_needing_reorder",
            "description": "List every product whose stock is below its reorder point.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_product_info",
            "description": "Get full details for a product by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "Stock code, e.g. 85123A"}
                },
                "required": ["product_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_reorder_point",
            "description": "Show the reorder point calculation breakdown for a product.",
            "parameters": {
                "type": "object",
                "properties": {"product_id": {"type": "string"}},
                "required": ["product_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_sales_trend",
            "description": "Show recent sales trend for a product over the last N days.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string"},
                    "days": {"type": "integer", "description": "Days to look back (default 30)"},
                },
                "required": ["product_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "simulate_scenario",
            "description": "Recalculate reorder point with a different lead time.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string"},
                    "new_lead_time": {"type": "integer"},
                },
                "required": ["product_id", "new_lead_time"],
            },
        },
    },
]

SYSTEM_PROMPT = """You are a stock reorder assistant.

You help users understand inventory data by calling tools.
Always call tools to get real numbers - never invent data.
When you answer, be clear and explain your reasoning briefly.
Format numbers cleanly (e.g. 123.4 not 123.40000001).
"""


def run_agent(user_input, max_steps=6, verbose=True):
    """Run the ReAct loop until the model produces a final answer."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    for step in range(max_steps):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS_SCHEMA,
            tool_choice="auto",
        )

        msg = response.choices[0].message

        if not msg.tool_calls:
            return msg.content

        messages.append(msg)

        for call in msg.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments) if call.function.arguments else {}
            if verbose:
                print(f"  [tool] {name}({args})")

            try:
                result = TOOLS[name](**args)
            except Exception as e:
                result = {"error": str(e)}

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result),
            })

    return "I reached the maximum number of steps without a final answer."


def chat_loop():
    """Interactive conversation."""
    print("Stock Reorder Agent (type 'exit' to quit)\n")
    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if user.lower() in {"exit", "quit", "sair"}:
            print("Bye!")
            break
        if not user:
            continue

        answer = run_agent(user)
        print(f"\nAgent: {answer}\n")


if __name__ == "__main__":
    chat_loop()

