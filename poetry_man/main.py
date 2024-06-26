import os
import subprocess
import json
import sys
from dotenv import load_dotenv
import llm
from termcolor import colored
from prompt import SYSTEM_PROMPT

def interact_with_user(message):
    print(colored(message, "cyan"))
    user_input = input("Your response: ")
    return json.dumps({
        "type": "user",
        "message": user_input
    })

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
        print(f"executing command:")
        print(colored(command, "green"))
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

    # Get the user prompt from CLI argument or ask the user
    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
    else:
        user_prompt = input("Hi! I'm poetry-man, the manager of poetry projects. How can I help you?\nYour message: ")

    # Wrap the user prompt in the appropriate format
    initial_prompt = json.dumps({
        "type": "user",
        "message": user_prompt
    })

    response = conversation.prompt(initial_prompt, system=SYSTEM_PROMPT)

    while not (response.get("dest") == "user" and response.get("message") == "Done!"):
        if response.get("dest") == "terminal":
            # Handle terminal command execution
            command_result = execute_command(response.get("message"))
            terminal_response = json.dumps({
                "type": "terminal",
                "message": json.loads(command_result)
            })
            response = conversation.prompt(terminal_response)
        elif response.get("dest") == "user":
            # Handle user interaction
            user_response = interact_with_user(response.get("message"))
            response = conversation.prompt(user_response)
        else:
            print("Invalid response destination")
            return
    print("Done!")
    
