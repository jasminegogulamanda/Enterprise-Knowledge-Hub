def retrieve_chunks(vector_store, question):

    docs = vector_store.similarity_search(
        question,
        k=3
    )

    context = ""

    sources = []

    for doc in docs:

        context += doc.page_content + "\n\n"

        sources.append({
            "file": doc.metadata["file"],
            "page": doc.metadata["page"]
        })

    return context, sources