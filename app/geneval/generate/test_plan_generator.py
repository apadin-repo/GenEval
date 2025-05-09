from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

class TestPlanGenerator:
    def __init__(self, system_prompt: str, context_prompt: str, docs: str, model_name: str, temperature: int):
        self.system_prompt = system_prompt
        self.context_prompt = context_prompt
        self.docs = docs
        self.llm = ChatOpenAI(temperature=temperature, model_name=model_name)

    def build_prompt(self, category) -> list:
        self.system_prompt = self.system_prompt.replace("[CATEGORY]", category)
        self.context_prompt = self.context_prompt.replace("[SYSTEM_DESCRIPTION]", self.docs or "No documentation provided.")
        return [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=self.context_prompt)
        ]

    def generate(self, category) -> str:
        prompt_messages = self.build_prompt(category)
        response = self.llm.invoke(prompt_messages)
        return response.content
