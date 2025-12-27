import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY NOT FOUND")

client = genai.Client(api_key=api_key)
model = "gemini-2.5-flash"
contents= "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
response = client.models.generate_content(model = model, contents = contents)

if not response.usage_metadata:
    raise RuntimeError("USAGE_METADATA IS NONE")

print(f"User prompt: {contents}")
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(f"Responses:\n{response.text}")