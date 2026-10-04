import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from config import LLM_CONFIG

# 1. 文档解析：读 3 个 txt
docs = []
for name in ["python.txt", "docker.txt", "travel.txt"]:
    loader = TextLoader(name, encoding="utf-8")
    docs += loader.load()
print(f"读入 {len(docs)} 个文档")

# 2. chunking：切成小块，每块 200 字、重叠 20 字
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = splitter.split_documents(docs)
print(f"切成 {len(chunks)} 块")

# 3. embedding：把每块变成向量，存进本地向量库 FAISS
embeddings = OpenAIEmbeddings(
    model=LLM_CONFIG["embedding_model"],
    api_key=LLM_CONFIG["api_key"],
    base_url=LLM_CONFIG["base_url"],
)
db = FAISS.from_documents(chunks, embeddings)
print("向量库建好")

# 4. 向量检索：问一个问题，找出最接近的 2 块
question = "Python 列表和字典有什么区别？"
results = db.similarity_search(question, k=2)

print("\n问题：", question)
for r in results:
    print("--- 命中片段 ---")
    print(r.page_content)