import os
import subprocess
import json
import sys
from dotenv import load_dotenv
import llm
from termcolor import colored
from prompt import SYSTEM_PROMPT
import re

def interact_with_user():
    user_input = input("Your response: ")
    return json.dumps({
        "type": "user",
        "message": user_input
    })

def execute_command(command):
    command_list = command.split()
    if ['sudo', 'rm', 'mv'] in command_list:
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
        process = subprocess.Popen(
            command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd(),  # Use the current working directory
            env=os.environ.copy()  # Use a copy of the current environment
        )
        stdout, stderr = process.communicate()
        return_code = process.returncode
        output = stdout if stdout else stderr
    except Exception as e:
        return_code = -1
        output = str(e)

    return json.dumps({
        "return_code": return_code,
        "message": output.strip()
    })

def search_for_tag(answer: str, tag: str) -> str:
    regex = f'<{tag}>(.*?)</{tag}>'
    match = re.search(regex, answer, re.DOTALL)
    if match:
        return match.group(1)
    return None

def prompt_json(conversation, prompt:str, system="")->json:
    responseObj = conversation.prompt(prompt) if system == "" else conversation.prompt(prompt, system=system)
    txt = responseObj.text()
    json_str = search_for_tag(txt, "JSON")
    if json_str == None :
        print(colored(f"Error no JSON tag found. txt: {txt}", "red"))

    try:
        json_obj = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(colored(f"Error decoding JSON: {e}", "red"))
        print(f"Problematic JSON string: {json_str}")
        return None

    return json_obj

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

    response = prompt_json(conversation, initial_prompt, SYSTEM_PROMPT)
    while True:
        if response["dest"] == "user":
            print(colored(response["message"], "green"))
            if response["message"] == "Done!":
                break
            user_response = interact_with_user()
            response = prompt_json(conversation, user_response, SYSTEM_PROMPT)
        elif response["dest"] == "terminal":
            # Handle terminal command execution
            command_result = execute_command(response["message"])
            terminal_response = json.dumps({
                "type": "terminal",
                "message": json.loads(command_result)
            }, indent=2)
            print(terminal_response)
            response = prompt_json(conversation, terminal_response, SYSTEM_PROMPT)
        else:
            print(colored("Invalid response destination", "red"))
            break
    
main()
