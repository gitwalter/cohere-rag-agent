import os
import streamlit as st

os.environ["COHERE_API_KEY"] = st.secrets["COHERE_API_KEY"]
QDRANT_HOST = st.secrets["QDRANT_HOST"]
QDRANT_API_KEY = st.secrets["QDRANT_API_KEY"]

# Streamlit header
st.set_page_config(page_title="Co:Chat - An LLM-powered chat bot")
st.title("ElsaBot")
st.write("This is a chatbot for out custom knowledge base")
