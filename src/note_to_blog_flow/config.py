import os
from textwrap import dedent

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

WEBSITE_URL = "https://www.example.com"

FILE_PATH = "./notes.md"

TITLE = "Advance CrewAI Setup for Best Long Format Content Creation Results"

TOPIC = "Advance CrewAI Setup for Best Long Format Content Creation Results"

GOAL = "To create a blog post sharing tips on effective CrewAI Flow setup to achieve the best long format content creation results."

WORD_COUNT = "2000"

WRITING_STYLE = "casual, personal but technically informative with simple vocabulary"

FLOW_INPUT_VARIABLES = {
    "title": TITLE,
    "topic": TOPIC,
    "goal": GOAL,
    "word_count": WORD_COUNT,
    "writing_style": WRITING_STYLE,
}
