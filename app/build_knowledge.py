from config.settings import Config
from knowledge.vectorstore.vector_store_builder import VectorStoreBuilder

vectorStore = VectorStoreBuilder(Config.DOCS_PATH,
                                 Config.CHROMA_PATH,
                                 Config.SUPPORTED_EXTENSIONS,
                                 Config.CHUNK_SIZE,
                                 Config.CHUNK_OVERLAP)

print("Building knowledge...")
documents = vectorStore.load_documents()
chunks = vectorStore.split_text(documents)
vectorStore.save_db(chunks)
print(f"Saved to vector store at {Config.CHROMA_PATH}.")
