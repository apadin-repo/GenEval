import os
from dotenv import load_dotenv
from loaders.yaml_loader import YAMLLoader
from langchain_community.document_loaders import PyPDFLoader

# Load environment variables from .env file
load_dotenv()

class Config:
    # LLMs API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # RAG Configuration
    CHROMA_PATH = "app/knowledge/chroma_db"
    DOCS_PATH = "app/knowledge/docs"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 300
    SUPPORTED_EXTENSIONS = {
        ".pdf": PyPDFLoader,
        ".yml": YAMLLoader,
        ".yaml": YAMLLoader
    }
    
    # Output
    OUTPUT_PATH = "output/"

Config = Config()
