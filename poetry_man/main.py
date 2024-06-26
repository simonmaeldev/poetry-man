import os
import subprocess
import json
from dotenv import load_dotenv
import llm
from termcolor import colored

def execute_command(command):
    command_list = command.split()
    if 'sudo' in command_list:
        print(colored("Warning: The bot is attempting to use sudo. This may require elevated privileges.", "red"))
    
    print(f"Command to execute: {command}")
    confirmation = input("Do you want to proceed? (y/n) [default: n]: ").lower()
    
    if confirmation != 'y':
        return json.dumps({
            "return_code": -1,
            "message": "Command execution cancelled by user."
        })

    try:
        result = subprocess.run(command_list, check=True, capture_output=True, text=True)
        return_code = result.returncode
        output = result.stdout
    except subprocess.CalledProcessError as e:
        return_code = e.returncode
        output = e.stderr

    return json.dumps({
        "return_code": return_code,
        "message": output.strip()
    })

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
    
