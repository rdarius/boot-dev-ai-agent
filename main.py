import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. 
You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. 
You do not need to specify the working directory in your function calls 
as it is automatically injected for security reasons.
"""

config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

messages = []

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def add_message(user, message):
    messages.append({"role": user, "parts": [{"text": message}]})

def main():
    if len(sys.argv) < 2:
        print("Error: No prompt provided.\nUsage: uv run main.py \"<your prompt here>\" [--verbose]")
        sys.exit(1)

    args = sys.argv[1:]

    verbose = False
    if "--verbose" in args:
        verbose = True
        args.remove("--verbose")

    user_prompt = " ".join(args)

    if verbose:
        print(f'User prompt: "{user_prompt}"')

    add_message("user", user_prompt)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=config,
    )

    if response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.function_call:
                function_call_part = part.function_call
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            elif part.text:
                reply_text = part.text

                # Add AI response to history
                add_message("model", reply_text)

                print(reply_text)

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()
