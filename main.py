import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def process_args():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg is None:
        print("Please provide a prompt as a command-line argument.")
        sys.exit(1)
    arg2 = sys.argv[2] if len(sys.argv) > 2 else None
    messages = [
        types.Content(role="user", parts=[types.Part(text=arg)]),
    ]
    return messages, arg, arg2



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages, arg, arg2 = process_args()
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
    )
    
    if arg2 is not None:
        print(f"User prompt: {arg}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")
    print(response.text)
    


main()
    
