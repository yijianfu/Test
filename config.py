from dotenv import load_dotenv
load_dotenv()
import os


def _get(key, default=None):
    """优先读 Streamlit Cloud 的 Secrets，本地开发回退到 .env / 环境变量。"""
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


LLM_CONFIG={
    "api_key": _get("OPENAI_API_KEY"),
    "model": _get("LLM_MODEL"),
    "base_url": _get("OPENAI_BASE_URL"),
    "embedding_model": _get("EMBEDDING_MODEL", "text-embedding-3-large"),
    "temperature": 0.7,
    "max_tokens": int(_get("LLM_MAX_TOKENS", 4000)),
}
