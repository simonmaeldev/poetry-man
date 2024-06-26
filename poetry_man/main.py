import os
from dotenv import load_dotenv
import llm

def main():
    load_dotenv()

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    model: llm.Model = llm.get_model("claude-3.5-sonnet")
    model.key = ANTHROPIC_API_KEY

    conversation=model.conversation()
    response = conversation.prompt("user prompt", system="system-prompt")
    