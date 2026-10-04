from dotenv import load_dotenv
load_dotenv()
import os

LLM_CONFIG={
    "api_key":os.getenv("OPENAI_API_KEY"),
    "model":os.getenv("LLM_MODEL"),
    "base_url":os.getenv("OPENAI_BASE_URL"),
    "embedding_model": os.getenv("EMBEDDING_MODEL", "text-embedding-3-large"),
    "temperature": 0.7,
    "max_tokens": int(os.getenv("LLM_MAX_TOKENS", 4000)),    
}
