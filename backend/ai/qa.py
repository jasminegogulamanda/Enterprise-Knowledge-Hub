import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-3.5-flash")


def ask_question(context, question):

    prompt = f"""
You are an Enterprise AI Assistant.

Answer ONLY from the given context.

If the answer is not available in the context, reply:

"I couldn't find this information in the document."

Context:
{context}

Question:
{question}
"""

    response = model.generate_content(prompt)

    return response.text