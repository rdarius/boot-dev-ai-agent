import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
        contents=messages
    )

    reply_text = response.text

    # Add AI response to history
    add_message("model", reply_text)

    print(reply_text)

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")



if __name__ == "__main__":
    main()
