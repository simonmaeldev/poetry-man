import os
from dotenv import load_dotenv
import llm

def main():
    load_dotenv()

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    model: llm.Model = llm.get_model("claude-3.5-sonnet")
    model.key = ANTHROPIC_API_KEY

    conversation = model.conversation()
    response = conversation.prompt("user prompt", system="system-prompt")

    while not (response.get("dest") == "user" and response.get("message") == "Done!"):
        if response.get("dest") == "terminal":
            # Handle terminal command execution
            pass
        elif response.get("dest") == "user":
            # Handle user interaction
            pass
        else:
            print("Invalid response destination")

        # Get next response (you'll need to implement this part)
        # response = get_next_response(conversation)
    
