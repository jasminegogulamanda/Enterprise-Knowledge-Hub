import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-3.5-flash")


def extract_keywords(text):

    prompt = f"""
Extract the 10 most important keywords from the following document.

Return only a bullet list.

Document:

{text}
"""

    response = model.generate_content(prompt)

    return response.text