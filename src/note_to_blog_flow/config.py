import os

# config.py
LLM_CONFIGS = {
    "openai": {
        "model": "gpt-4o-mini",
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
    "anthropic": {
        "model": "anthropic/claude-3-5-sonnet-20240620",
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
    },
}

LANGTRACE_API_KEY = os.getenv("LANGTRACE_API_KEY")

FILE_PATH = "./notes.md"
