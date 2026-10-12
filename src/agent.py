"""
Stock Reorder Assistant - conversational agent.

Uses Groq (GPT-OSS 120B) with tool calling to answer
business questions about inventory in natural language.

Supports English, Portuguese and Spanish.
Keeps conversation memory (last N messages).
"""

import json
import os
import re
import time

from dotenv import load_dotenv
from groq import Groq

from agent_tools import TOOLS

load_dotenv()


def _get_groq_key():
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


# ============================================================
# TOOL SCHEMA
# ============================================================
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


# ============================================================
# LANGUAGE DETECTION
# ============================================================
def detect_language(text: str) -> str:
    """Detect EN / PT / ES. Defaults to EN."""
    try:
        from langdetect import detect, DetectorFactory
        DetectorFactory.seed = 0
        lang = detect(text)
        if lang in ("pt", "es", "en"):
            return lang
        if lang in ("ca", "gl"):
            return "pt"
        return "en"
    except Exception:
        return "en"


# ============================================================
# SYSTEM PROMPT
# ============================================================
SYSTEM_PROMPT = """You are a stock reorder assistant for a retail inventory system.

You help users understand inventory data by calling tools.
ALWAYS call tools to get real numbers - never invent data.

LANGUAGE RULES (highest priority):
- Detect the language of the user's question.
- If the question is in English, answer in English.
- If the question is in Portuguese, answer in Portuguese (pt-PT).
- If the question is in Spanish, answer in Spanish (es-ES).
- If mixed or unclear, default to English.

STYLE:
- Clear, professional, concise.
- Explain your reasoning briefly.
- Format numbers cleanly (e.g. 123.4 not 123.40000001).
"""


# ============================================================
# RUN AGENT (tool-calling loop) - retained for compatibility
# ============================================================
def run_agent(user_input, max_steps=6, verbose=True, history=None):
    """Run the ReAct loop until the model produces a final answer."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if history:
        for h in history[-6:]:
            role = h.get("role", "user")
            content = h.get("content", "")
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_input})

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


# ============================================================
# ASK - main entry point (returns rich dict)
# ============================================================
def ask(question: str, verbose: bool = False, history: list = None) -> dict:
    """Main entry point. Returns a dict compatible with the Inditex agent."""
    start = time.time()
    lang = detect_language(question)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if history:
        for h in history[-6:]:
            role = h.get("role", "user")
            content = h.get("content", "")
            if role in ("user", "assistant") and content:
                messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": question})

    tools_used = []
    max_steps = 6

    for step in range(max_steps):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS_SCHEMA,
                tool_choice="auto",
            )
        except Exception as e:
            return {
                "explanation": f"Error: {e}",
                "error": str(e),
                "language": lang,
                "tool_calls": [],
                "steps": step + 1,
                "duration_ms": int((time.time() - start) * 1000),
            }

        msg = response.choices[0].message

        if not msg.tool_calls:
            duration_ms = int((time.time() - start) * 1000)
            return {
                "explanation": msg.content or "",
                "language": lang,
                "tool_calls": tools_used,
                "steps": step + 1,
                "duration_ms": duration_ms,
            }

        messages.append(msg)

        for call in msg.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments) if call.function.arguments else {}

            try:
                result = TOOLS[name](**args)
            except Exception as e:
                result = {"error": str(e)}

            tools_used.append({
                "name": name,
                "args": args,
                "result": result,
            })

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result),
            })

    return {
        "explanation": "I reached the maximum number of steps without a final answer.",
        "language": lang,
        "tool_calls": tools_used,
        "steps": max_steps,
        "duration_ms": int((time.time() - start) * 1000),
    }


# ============================================================
# CLI (interactive) - optional
# ============================================================
def chat_loop():
    print("Stock Reorder Agent (type 'exit' to quit)\n")
    history = []
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

        result = ask(user, history=history)
        print(f"\nAgent: {result['explanation']}\n")

        history.append({"role": "user", "content": user})
        history.append({"role": "assistant", "content": result["explanation"]})


if __name__ == "__main__":
    chat_loop()