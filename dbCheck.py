import qdrant_client
import streamlit as st


QDRANT_HOST = st.secrets["QDRANT_HOST"]
QDRANT_API_KEY = st.secrets["QDRANT_API_KEY"]


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
