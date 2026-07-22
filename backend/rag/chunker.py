from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_text(pages):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    all_chunks = []

    for page in pages:

        chunks = splitter.split_text(page["text"])

        for chunk in chunks:

            all_chunks.append({
                "text": chunk,
                "page": page["page"],
                "file": page["file"]
            })

    return all_chunks