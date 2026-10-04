from openai import OpenAI
from langchain_openai import ChatOpenAI
from config import LLM_CONFIG


def get_client():
    client = OpenAI(
        api_key=LLM_CONFIG["api_key"], 
        base_url=LLM_CONFIG["base_url"],
    )
    return client

def get_llm():
    llm = ChatOpenAI(
        model=LLM_CONFIG["model"],     
        api_key=LLM_CONFIG["api_key"], 
        base_url=LLM_CONFIG["base_url"],
        temperature=0,  
    )
    return llm


# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "你是一个耐心的老师，用大白话回答新手的问题。"},
#         {"role": "user", "content": "用一句话解释：什么是 API？"}
#     ],
#     temperature=0.7
# )

# print(response.choices[0].message.content)
