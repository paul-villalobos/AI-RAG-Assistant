from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate

def  rephase_prompt(system_prompt: str, user_prompt: str) -> ChatPromptTemplate:
        rephrase= ChatPromptTemplate([
        SystemMessage(content=system_prompt),
        ("user", user_prompt)
        ])
        return rephrase