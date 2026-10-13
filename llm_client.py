import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Verify API key is present
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY is not set. Please add it to your .env file.")

# Initialize client
client = genai.Client()

def ask_gemini(
    system_prompt: str, 
    user_prompt: str, 
    model: str = "gemini-2.5-flash",
    temperature: float = 0.2
) -> str:
    """Sends system and user prompt to Gemini with controlled temperature for grounded responses."""
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=temperature
    )
    
    response = client.models.generate_content(
        model=model,
        contents=user_prompt,
        config=config
    )
    
    return response.text

