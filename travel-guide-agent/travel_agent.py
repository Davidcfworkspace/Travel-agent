# travel_agent.py
import os, sys, json, datetime as dt, textwrap
from typing import Dict, Any, List, Optional
import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# ---------- setup ----------
console = Console()
load_dotenv()  # loads variables from .env file

from openai import OpenAI

# Get your API key from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
if not OPENAI_API_KEY:
    console.print("[bold red]Error:[/bold red] OPENAI_API_KEY not found in .env")
    sys.exit(1)

# Create OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# ---------- System Prompt ----------
SYS_PROMPT = """You are a friendly and knowledgeable travel guide.
You provide detailed, practical, and inspiring recommendations for trips,
including itineraries, weather forecast on trip days cultural insights, and travel tips. 
Take weather and other aspects in consideration before recommending the activity. Be sure to warn
users of the dangers of traveling to a location make that apparent from the start.
Be concise but helpful, and tailor your advice to the user's request."""

# ---------- helper: call GPT ----------
def compose_with_openai(user_prompt: str, sys_prompt: str = SYS_PROMPT) -> str:
    """
    Sends a prompt to OpenAI and returns the assistant's reply.
    """
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # lightweight + fast
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenAI: {e}"

# ---------- CLI runner ----------
if __name__ == "__main__":
    console.print(Panel("🌍 Welcome to the Travel Guide Agent!", style="bold blue"))

    while True:
        try:
            user_prompt = console.input("\n[bold green]Ask about a trip (or type 'quit'): [/bold green]")
            if user_prompt.lower() in ["quit", "exit", "q"]:
                console.print("[bold red]Goodbye![/bold red]")
                break

            reply = compose_with_openai(user_prompt)
            console.print(Panel(reply, title="Your Travel Guide", expand=False, style="cyan"))
        except KeyboardInterrupt:
            console.print("\n[bold red]Goodbye![/bold red]")
            break
