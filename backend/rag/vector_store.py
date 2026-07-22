from langchain_community.vectorstores import FAISS


def create_vector_store(chunks, embeddings):

    texts = []
    metadatas = []

    for chunk in chunks:

        texts.append(chunk["text"])

        metadatas.append({
            "page": chunk["page"],
            "file": chunk["file"]
        })

    vector_store = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )

    return vector_store