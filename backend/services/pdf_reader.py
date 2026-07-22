import fitz

def extract_text(uploaded_file):

    pdf = fitz.open(
        stream=uploaded_file.read(),
        filetype="pdf"
    )

    full_text = ""
    pages = []

    for page_no, page in enumerate(pdf):

        text = page.get_text()

        full_text += text + "\n"

        pages.append({
            "page": page_no + 1,
            "text": text,
            "file": uploaded_file.name
        })

    pdf.close()

    return full_text, pages