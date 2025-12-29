import argparse
import os
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
        config=types.GenerateContentConfig(system_instruction=system_prompt),   
    )

    if not response.usage_metadata:
        raise RuntimeError("USAGE_METADATA IS NONE")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(f"Responses:\n{response.text}")

if __name__ == "__main__":
    main()