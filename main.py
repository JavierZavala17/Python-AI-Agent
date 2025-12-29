import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    # Accept user input
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    # Activate verbose responses
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()  # Now we can access `args.user_prompt`

    # Load GEMINI_API_KEY
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    
    # Initiate call to GEMINI
    client = genai.Client(api_key=api_key)
    # Array that will contain the conversation with GEMINI
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\\n")


    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model = "gemini-2.5-flash", 
        contents = messages,
        config = types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction = system_prompt,
        ),
    )

    if not response.usage_metadata:
        raise RuntimeError("USAGE_METADATA IS NONE")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if not response.function_calls:
        print(f"Responses:\n{response.text}")
        return
    
    function_results = []
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
        function_call_result = call_function(function_call, verbose=verbose)

        if not function_call_result.parts:
            raise Exception("...parts is empty...")
        
        first_part = function_call_result.parts[0]

        if first_part.function_response is None:
            raise Exception("...function_response is None...")
        
        if first_part.function_response.response is None:
            raise Exception("...response is None...")
        
        function_results.append(first_part)

        if verbose:
            print(f"-> {first_part.function_response.response}")
        
    
if __name__ == "__main__":
    main()