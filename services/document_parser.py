from pathlib import Path

import fitz
from docx import Document


def extract_pdf_pages(file_path: str):
    """
    Extract text page-by-page from a PDF.

    Returns:
        [
            {
                "page_number": 1,
                "text": "..."
            },
            ...
        ]
    """

    pages = []

    document = fitz.open(file_path)

    try:
        for page_number, page in enumerate(document, start=1):

            text = page.get_text("text").strip()

            if text:
                pages.append(
                    {
                        "page_number": page_number,
                        "text": text
                    }
                )

    finally:
        document.close()

    return pages


def extract_docx_pages(file_path: str):
    """
    DOCX does not have a reliable page concept at the
    document structure level.

    For this project, the complete document is treated
    as page 1.
    """

    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    text = "\n".join(paragraphs)

    if not text:
        return []

    return [
        {
            "page_number": 1,
            "text": text
        }
    ]


def extract_txt_pages(file_path: str):
    """
    Extract text from TXT files.
    """

    text = Path(file_path).read_text(
        encoding="utf-8"
    ).strip()

    if not text:
        return []

    return [
        {
            "page_number": 1,
            "text": text
        }
    ]


def extract_document(file_path: str):
    """
    Automatically detect the document type and extract text.
    """

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":

        return extract_pdf_pages(file_path)

    if extension == ".docx":

        return extract_docx_pages(file_path)

    if extension == ".txt":

        return extract_txt_pages(file_path)

    raise ValueError(
        f"Unsupported document type: {extension}"
    )