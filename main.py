import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from function_declaration import available_functions
from prompts import system_prompt
from functions.call_function import call_function

def generate_content(client, messages, verbose):
    
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            break
        except Exception as e:
            if attempt == 4:
                print(f"Error: {e}")
                raise Exception("Max retries exceeded")
            
            delay = 2 * 2**attempt
            print(f"Error: {e}. Attempt {(attempt + 2)}/{5}. Retrying in {delay} seconds...")
    
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)
            
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        function_response = call_function(function_call_part, verbose)
        #messages.append(types.Content(role="user", parts=function_response))
        messages.append(function_response)
        if not function_response.parts[0].function_response.response:
            raise Exception("No function response received")
        




def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    try:
        for i in range(20):
            result = generate_content(client, messages, verbose)
            if result:
                print("\nResult:\n", result)
                break
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
    


main()
    
