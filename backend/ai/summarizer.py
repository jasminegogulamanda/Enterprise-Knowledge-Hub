import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(api_key)

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-3.5-flash")

def summarize_text(text):
    prompt = f"""
You are an AI assistant.

Summarize the following document in simple English.

Document:
{text}
"""

    response = model.generate_content(prompt)

    return response.text