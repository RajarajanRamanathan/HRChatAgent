from pathlib import Path

import chromadb
from google import genai
from google.genai import types

from config.settings import (
    CHROMA_PATH,
    CHROMA_COLLECTION_NAME,
    EMBEDDING_MODEL,
    EMBEDDING_DIMENSION,
    GEMINI_API_KEY
)

from services.document_parser import extract_document


# ============================================================
# Gemini Client
# ============================================================

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to the .env file."
    )


gemini_client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# ChromaDB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = chroma_client.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME,
    metadata={
        "description": "HR policy knowledge base"
    }
)


# ============================================================
# Chunking
# ============================================================

def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap: int = 200
):
    """
    Split text into overlapping chunks.

    Character-based chunking is sufficient for this
    capstone project and keeps the implementation simple.
    """

    text = text.strip()

    if not text:
        return []

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(
            start + chunk_size,
            text_length
        )

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - overlap

    return chunks


# ============================================================
# Policy Name
# ============================================================

def get_policy_name(file_name: str):
    """
    Convert file name into a readable policy name.
    """

    return Path(file_name).stem.replace(
        "_",
        " "
    )


# ============================================================
# Policy Type
# ============================================================

def get_policy_type(file_name: str):
    """
    Determine policy type from the file name.
    """

    name = Path(file_name).stem.lower()

    if "leave" in name:
        return "Leave"

    if "attendance" in name:
        return "Attendance"

    if "work_from_home" in name or "wfh" in name:
        return "Work From Home"

    if "travel" in name:
        return "Travel"

    if "maternity" in name:
        return "Maternity"

    return "General"


# ============================================================
# Gemini Embedding
# ============================================================

def generate_embedding(text: str):
    """
    Generate a Gemini Embedding 2 vector.

    We use the question-answering retrieval format
    recommended for semantic retrieval.
    """

    content = (
        "title: HR Policy | "
        f"text: {text}"
    )

    result = gemini_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=content,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSION
        )
    )

    return result.embeddings[0].values


# ============================================================
# Build Knowledge Base
# ============================================================

def build_policy_knowledge_base():
    """
    Read all policy documents and store their embeddings
    in ChromaDB.

    Returns:
        {
            "documents": number of source documents,
            "chunks": number of chunks
        }
    """

    policy_directory = Path(
        "policy_documents"
    )

    policy_directory.mkdir(
        exist_ok=True
    )

    files = []

    for extension in [
        "*.pdf",
        "*.docx",
        "*.txt"
    ]:
        files.extend(
            policy_directory.glob(extension)
        )

    if not files:
        return {
            "documents": 0,
            "chunks": 0
        }

    # --------------------------------------------------------
    # Remove existing records.
    #
    # This keeps rebuilding deterministic during development.
    # --------------------------------------------------------

    existing = collection.get()

    if existing and existing.get("ids"):

        collection.delete(
            ids=existing["ids"]
        )

    total_chunks = 0

    for file_path in files:

        document_name = file_path.name

        policy_name = get_policy_name(
            document_name
        )

        policy_type = get_policy_type(
            document_name
        )

        pages = extract_document(
            str(file_path)
        )

        for page in pages:

            page_number = page[
                "page_number"
            ]

            page_text = page[
                "text"
            ]

            chunks = chunk_text(
                page_text
            )

            for chunk_index, chunk in enumerate(
                chunks
            ):

                embedding = generate_embedding(
                    chunk
                )

                document_id = (
                    f"{document_name}_"
                    f"page_{page_number}_"
                    f"chunk_{chunk_index}"
                )

                metadata = {
                    "document": document_name,
                    "policy_name": policy_name,
                    "policy_type": policy_type,
                    "page_number": page_number,
                    "chunk_index": chunk_index,
                    "source": document_name
                }

                collection.add(
                    ids=[document_id],
                    documents=[chunk],
                    embeddings=[embedding],
                    metadatas=[metadata]
                )

                total_chunks += 1

    return {
        "documents": len(files),
        "chunks": total_chunks
    }


# ============================================================
# Search Policies
# ============================================================

def search_hr_policies(
    question: str,
    top_k: int = 5
):
    """
    Search HR policies using semantic similarity.
    """

    query_text = (
        "task: question answering | "
        f"query: {question}"
    )

    result = gemini_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=query_text,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSION
        )
    )

    query_embedding = result.embeddings[0].values

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    matches = []

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    for index, document in enumerate(
        documents
    ):

        metadata = metadatas[index]

        distance = (
            distances[index]
            if index < len(distances)
            else None
        )

        matches.append(
            {
                "content": document,
                "document": metadata.get(
                    "document"
                ),
                "policy_name": metadata.get(
                    "policy_name"
                ),
                "policy_type": metadata.get(
                    "policy_type"
                ),
                "page_number": metadata.get(
                    "page_number"
                ),
                "chunk_index": metadata.get(
                    "chunk_index"
                ),
                "distance": distance
            }
        )

    return matches


# ============================================================
# Knowledge Base Statistics
# ============================================================

def get_policy_statistics():

    result = collection.get()

    ids = result.get(
        "ids",
        []
    )

    return {
        "chunks": len(ids)
    }