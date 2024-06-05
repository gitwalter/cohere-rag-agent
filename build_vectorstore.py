import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Qdrant
from langchain_cohere import CohereEmbeddings
import streamlit as st



os.environ["COHERE_API_KEY"] = st.secrets["COHERE_API_KEY"]
QDRANT_HOST = st.secrets["QDRANT_HOST"]
QDRANT_API_KEY = st.secrets["QDRANT_API_KEY"]


web_links = ["https://python.langchain.com/v0.2/docs/introduction",
             "https://python.langchain.com/v0.2/docs/concepts",
             "https://python.langchain.com/v0.2/docs/integrations/tools",
             "https://python.langchain.com/v0.2/docs/integrations/vectorstores",
             "https://python.langchain.com/v0.2/docs/integrations/document_loaders",
             "https://python.langchain.com/v0.2/docs/integrations/retrievers",
             "https://python.langchain.com/v0.2/docs/integrations/vectorstores/qdrant",
             "https://python.langchain.com/v0.2/docs/integrations/providers/cohere/#react-agent"]
 

loader = WebBaseLoader(web_links)
document=loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
texts = text_splitter.split_documents(document)

embeddings = CohereEmbeddings(model = "embed-english-v2.0")

qdrant = Qdrant.from_documents(
    document,
    embeddings,
    url=QDRANT_HOST,
    api_key=QDRANT_API_KEY,
    prefer_grpc=True,
    collection_name="rag_documents",
    force_recreate=True,
)
