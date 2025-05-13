from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from geneval.generate.prompts import Prompts
from config.settings import Config
from io import StringIO
import pandas as pd

class TestPlan:
    def __init__(self): 
        self.__system_prompt_template = Prompts.SYSTEM_PROMPT
        self.__context_prompt_template = Prompts.SYSTEM_CONTEXT
        self.__llm = ChatOpenAI(temperature=Config.TEMPERATURE, model_name=Config.MODEL)

    def __build_prompt(self, category, context) -> list:
        self.__system_prompt = self.__system_prompt_template.replace("[CATEGORY]", category)
        self.__context_prompt = self.__context_prompt_template.replace("[SYSTEM_DESCRIPTION]", context or "No documentation provided.")
        return [
            SystemMessage(content=self.__system_prompt),
            HumanMessage(content=self.__context_prompt)
        ]

    def generate(self, context) -> pd.DataFrame:
        dfs = []

        for category in Prompts.CATEGORIES:
            prompt_messages = self.__build_prompt(category, context)
            output = self.__llm.invoke(prompt_messages)
            csv_text = output.content.strip()
           
            try:
                df = pd.read_csv(StringIO(csv_text))
                dfs.append(df)
            except Exception as e:
                print(f"Failed to parse CSV for category {category}: {e}")
                continue
        
        if not dfs:
            return pd.DataFrame([]) # empty df
    
        return pd.concat(dfs, ignore_index=True)
    

TestPlan = TestPlan()
