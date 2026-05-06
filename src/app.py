import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from src.rag.generator import generate_answer

load_dotenv()

st.set_page_config(page_title="Rag Assistant", page_icon="🤖", layout="centered")
st.title("🤖 Assistant (RAG)")

if not os.environ.get("OPENAI_API_KEY"):
    st.error("❌ Missing OPENAI_API_KEY. Please add it to your .env file!")
    st.stop() 

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    
    with st.chat_message(role):
        st.markdown(msg.content)

query = st.chat_input("Type your question here...")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    
    with st.spinner("Searching documents..."):
        try:
            answer = generate_answer(query, st.session_state.chat_history)
            
            with st.chat_message("assistant"):
                st.markdown(answer)
            
            st.session_state.chat_history.append(HumanMessage(content=query))
            st.session_state.chat_history.append(AIMessage(content=answer))
            
        except Exception as e:
            st.error(f"An error occurred in the RAG system: {e}")