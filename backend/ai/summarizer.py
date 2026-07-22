import os
import streamlit as st
import google.generativeai as genai

api_key = st.secrets["GOOGLE_API_KEY"]

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