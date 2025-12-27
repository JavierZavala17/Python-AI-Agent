import argparse
import os
from dotenv import load_dotenv
from google import genai

# Load GEMINI_API_KEY
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY NOT FOUND")

# Accept user input
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()
# Now we can access `args.user_prompt`

# Initiate call to GEMINI
client = genai.Client(api_key=api_key)
model = "gemini-2.5-flash"
response = client.models.generate_content(model = model, contents = args.user_prompt)

if not response.usage_metadata:
    raise RuntimeError("USAGE_METADATA IS NONE")

print(f"User prompt: {args.user_prompt}")
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(f"Responses:\n{response.text}")