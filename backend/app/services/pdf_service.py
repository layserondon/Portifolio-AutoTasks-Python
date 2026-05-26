import fitz


def extract_text_from_pdf(content: bytes) -> str:
    text = ""

    with fitz.open(stream=content, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text
