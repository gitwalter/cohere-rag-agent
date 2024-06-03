import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.vectorstores import Qdrant
import streamlit as st
import qdrant_client



os.environ["COHERE_API_KEY"] = st.secrets["COHERE_API_KEY"]
QDRANT_HOST = st.secrets["QDRANT_HOST"]
QDRANT_API_KEY = st.secrets["QDRANT_API_KEY"]



web_links = ["https://www.fielmann-group.com/ueber-uns/?",
             "https://de.wikipedia.org/wiki/Fielmann",
             "https://de.wikipedia.org/wiki/G%C3%BCnther_Fielmann",
             "https://de.wikipedia.org/wiki/Marc_Fielmann"] 

loader = WebBaseLoader(web_links)
document=loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
texts = text_splitter.split_documents(document)

embeddings = CohereEmbeddings(model = "embed-english-v2.0")


# Creating a persistant DB
client = qdrant_client.QdrantClient(
    url = QDRANT_HOST,
    api_key= QDRANT_API_KEY,
)
# create_collection
collection_name = "rag_documents"
vector_config = qdrant_client.http.models.VectorParams(
    size = 4096,
    distance = qdrant_client.http.models.Distance.COSINE
)
client.recreate_collection(
    collection_name = collection_name,
    vectors_config = vector_config,
)

vector_store = Qdrant(
    client=client,
    collection_name = collection_name,
    embeddings=embeddings
)
vector_store.add_documents(texts)
