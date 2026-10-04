import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from config import LLM_CONFIG
from chat import get_llm

embeddings = OpenAIEmbeddings(
    model=LLM_CONFIG["embedding_model"],
    api_key=LLM_CONFIG["api_key"],
    base_url=LLM_CONFIG["base_url"],
)

# 1. 加载 + 切块（第 6 课同款）
docs = []
for name in ["python.txt", "docker.txt", "travel.txt"]:
    docs += TextLoader(name, encoding="utf-8").load()
chunks = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20).split_documents(docs)

# 2. 存进 ChromaDB（持久化到 ./chroma_db 文件夹，重启不丢）
db = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
print(f"向量库建好，共 {db._collection.count()} 块")

# 3. 检索：拿最相关的 2 块
question = "怎么修汽车？"
hits = db.similarity_search(question, k=2)

# 4. 把片段拼进提示词（第 3 课学的！来源写进括号里）
context = "\n\n".join(f"[来源 {h.metadata['source']}]\n{h.page_content}" for h in hits)
prompt = f"""你是一个知识库问答助手。请只根据下面的资料回答问题。
如果资料里没有答案，就说"资料中没有相关信息"，不要编造。

资料：
{context}

问题：{question}"""

# 5. DeepSeek 回答（第 2 课学的调用）
llm = get_llm()
answer = llm.invoke(prompt).content

print("\n回答：", answer)
print("\n引用来源：")
for h in hits:
    print(" -", h.metadata["source"])