import streamlit as st

def upload_pdf():

    uploaded_files = st.file_uploader(
        "📂 Upload PDF Documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    return uploaded_files