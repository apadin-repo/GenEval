import os
from dotenv import load_dotenv
from loaders.yaml_loader import YAMLLoader
from langchain_community.document_loaders import PyPDFLoader, TextLoader

# Load environment variables from .env file
load_dotenv()

class Config:
    # LLMs API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # LLM Configuration
    TEMPERATURE = 0
    MAX_TOKENS = ''
    MAX_NEW_TOKENS = ''
    MODEL = "gpt-4o-mini"

    # RAG Configuration
    CHROMA_PATH = "app/knowledge/chroma_db"
    DOCS_PATH = "app/knowledge/docs"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 300
    SUPPORTED_EXTENSIONS = { # future: docs, excel, .txt, powerpoint, 
        ".pdf": PyPDFLoader,
        ".yml": YAMLLoader,
        ".yaml": YAMLLoader,
        ".md": TextLoader
    }
    
    # Output
    OUTPUT_PATH = "output/"

Config = Config()
