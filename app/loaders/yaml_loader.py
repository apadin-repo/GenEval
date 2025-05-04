import yaml
from typing import List
from langchain_core.documents import Document

class YAMLLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> List[Document]:
        with open(self.file_path, 'r') as f:
            content = yaml.safe_load(f)
        return [Document(page_content=str(content))]
