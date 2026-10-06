import os

from dotenv import load_dotenv


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

EMBEDDING_MODEL = "gemini-embedding-2"

EMBEDDING_DIMENSION = 768

CHROMA_PATH = "chroma_db"

CHROMA_COLLECTION_NAME = "hr_policy_documents"

POLICY_DOCUMENT_PATH = "policy_documents"