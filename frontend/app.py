import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from components.pdf_upload import upload_pdf

from backend.services.pdf_reader import extract_text

from backend.ai.summarizer import summarize_text
from backend.ai.qa import ask_question
from backend.ai.keywords import extract_keywords

from backend.rag.chunker import split_text
from backend.rag.embeddings import get_embeddings
from backend.rag.vector_store import create_vector_store
from backend.rag.retrieval import retrieve_chunks


@st.cache_resource
def load_vector_store(all_pages):

    chunks = split_text(all_pages)
    embeddings = get_embeddings()

    vector_store = create_vector_store(
        chunks,
        embeddings
    )

    return vector_store, chunks


st.set_page_config(
    page_title="Enterprise Knowledge Hub",
    page_icon="📚",
    layout="wide"
)
if "messages" not in st.session_state:
    st.session_state.messages = []
with st.sidebar:

    st.title("📚 Enterprise Knowledge Hub")

    st.markdown("---")

    st.write("### 🚀 Features")

    st.success("✅ Multiple PDF Upload")
    st.success("✅ AI Summary")
    st.success("✅ AI Q&A")
    st.success("✅ Keyword Extraction")
    st.success("✅ RAG Search")
    st.success("✅ Source Citation")

    st.markdown("---")

    st.write("### 👨‍💻 Developer")

    st.info("Jasmine Gogulamanda")
    st.markdown("---")

    if st.button("🗑️ Clear Chat"):

       st.session_state.messages = []
       st.success("Chat cleared successfully!")


st.title("📚 Enterprise Knowledge Hub")

st.markdown("""
### 🤖 AI-Powered Enterprise Document Intelligence

Upload multiple PDFs, generate summaries, ask questions, extract keywords, and perform semantic search using RAG + Gemini AI.
""")



uploaded_files = upload_pdf()

if uploaded_files:

    all_text = ""
    all_pages = []

    for pdf in uploaded_files:

        text, pages = extract_text(pdf)

        all_text += text + "\n"

        all_pages.extend(pages)

    st.success(f"✅ {len(uploaded_files)} PDF(s) Uploaded Successfully")

    vector_store, chunks = load_vector_store(all_pages)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📂 PDFs", len(uploaded_files))

    with col2:
        st.metric("📄 Pages", len(all_pages))

    with col3:
        st.metric("✂ Chunks", len(chunks))
    st.info(f"📄 Total Chunks Created : {len(chunks)}")

    st.subheader("📄 Extracted Text")

    st.text_area(
        "Document Content",
        all_text,
        height=300
    )

    st.divider()

    st.subheader("📑 AI Summary")

    if st.button("✨ Generate Summary"):

        with st.spinner("Generating Summary..."):

            summary = summarize_text(all_text)

        st.success("Summary Generated!")

        st.write(summary)
        st.download_button(
            label="⬇ Download Summary",
            data=summary,
            file_name="AI_Summary.txt",
            mime="text/plain"
        )

    st.divider()

    st.subheader("💬 Chat with Your Documents")

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "sources" in message:

                st.markdown("### 📄 Sources")

                shown = set()

                for source in message["sources"]:

                    key = (source["file"], source["page"])

                    if key not in shown:

                      shown.add(key)

                      st.write(f"📄 {source['file']} | Page {source['page']}")

    question = st.chat_input("Ask anything about your documents...")

    if question:

        st.session_state.messages.append(
          {
            "role": "user",
            "content": question
          }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.spinner("Searching Documents..."):

            context, sources = retrieve_chunks(
            vector_store,
            question
            )

            answer = ask_question(
            context,
            question
            )

        st.session_state.messages.append(
          {
            "role": "assistant",
            "content": answer,
            "sources": sources
          }
        )

        with st.chat_message("assistant"):

           st.markdown(answer)

           st.markdown("### 📄 Sources")

           shown = set()

           for source in sources:

              key = (source["file"], source["page"])

              if key not in shown:

                 shown.add(key)

                 st.write(
                    f"📄 {source['file']} | Page {source['page']}"
                 )

    st.divider()

    st.subheader("🔑 Extract Keywords")

    if st.button("🔑 Extract Keywords"):

        with st.spinner("Extracting Keywords..."):

            keywords = extract_keywords(all_text)

        st.write(keywords)