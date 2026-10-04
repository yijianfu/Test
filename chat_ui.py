import os
import streamlit as st
from openai import OpenAI
from chat import get_client
from config import LLM_CONFIG

client = get_client()

st.set_page_config(page_title="我的 AI 助手", page_icon="🤖")
st.title("🤖 我的第一个 AI 网页应用")

# ---- 记忆抽屉：聊天记录放这里，刷新也不丢 ----
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---- 回放历史：把已有对话画成气泡 ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- 输入框：用户敲回车触发 ----
if prompt := st.chat_input("输入你的问题……"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 调 LLM：带整段历史 = 多轮对话
    with st.chat_message("assistant"):
        with st.spinner("思考中……"):
            resp = client.chat.completions.create(
                model=LLM_CONFIG["model"],
                messages=st.session_state.messages,
            )
            answer = resp.choices[0].message.content
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})