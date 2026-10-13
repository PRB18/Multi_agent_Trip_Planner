import os
from dotenv import load_dotenv
from google import genai


load_dotenv()
# Initialize the client
# It automatically looks for the GEMINI_API_KEY environment variable
client = genai.Client()

# Make the LLM call
def ask_gemini(system_prompt: str, user_prompt: str)-> str:
    response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=user_prompt,
    config = {
        "system_instruction": system_prompt
    }
)

    return response.text

