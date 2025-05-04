import os
import glob
import shutil
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

class VectorStoreBuilder:
    def __init__(self, docs_path, chroma_path, supported_extensions, chunk_size, chunk_overlap):
        self.docs_path: str = docs_path
        self.chroma_path: str = chroma_path
        self.supported_extensions: list = supported_extensions
        self.chunk_size: int = chunk_size
        self.chunk_overlap: int = chunk_overlap

    def load_documents(self):
        documents = []
        for ext, LoaderClass in self.supported_extensions.items():
            for path in glob.glob(f"{self.docs_path}/*{ext}"):
                try:
                    loader = LoaderClass(path)
                    documents.extend(loader.load())
                except Exception as e:
                    print(f"Error loading {ext.upper()} file {path}: {e}")
        return documents
    
    def split_text(self, documents):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            add_start_index=True
        )
        return text_splitter.split_documents(documents)
    
    def save_db(self, chunks):
        if os.path.exists(self.chroma_path):
            shutil.rmtree(self.chroma_path)

        db = Chroma.from_documents(
            documents=chunks,
            embedding=OpenAIEmbeddings(),
            persist_directory=self.chroma_path
        )
