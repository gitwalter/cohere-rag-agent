import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.vectorstores import Qdrant
import streamlit as st
# import qdrant_client
from langchain_community.vectorstores import Qdrant


os.environ["COHERE_API_KEY"] = st.secrets["COHERE_API_KEY"]
QDRANT_HOST = st.secrets["QDRANT_HOST"]
QDRANT_API_KEY = st.secrets["QDRANT_API_KEY"]



# web_links = ["https://www.fielmann-group.com/ueber-uns/?",
#              "https://de.wikipedia.org/wiki/Fielmann",
#              "https://de.wikipedia.org/wiki/G%C3%BCnther_Fielmann",
#              "https://de.wikipedia.org/wiki/Marc_Fielmann"] 

web_links = ["https://python.langchain.com/v0.2/docs/introduction",
             "https://python.langchain.com/v0.2/docs/concepts",
             "https://python.langchain.com/v0.2/docs/integrations/tools",
             "https://python.langchain.com/v0.2/docs/integrations/vectorstores",
             "https://python.langchain.com/v0.2/docs/integrations/document_loaders",
             "https://python.langchain.com/v0.2/docs/integrations/retrievers",
             "https://python.langchain.com/v0.2/docs/integrations/vectorstores/qdrant",
             "https://python.langchain.com/v0.2/docs/integrations/providers/cohere/#react-agent",
             "https://de.wikipedia.org/wiki/Herz#:~:text=Das%20Herz%20(lateinisch%20Cor%2C%20griechisch,die%20Versorgung%20aller%20Organe%20sichert."]
 

loader = WebBaseLoader(web_links)
document=loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
texts = text_splitter.split_documents(document)

embeddings = CohereEmbeddings(model = "embed-english-v2.0")


# # Creating a persistant DB
# client = qdrant_client.QdrantClient(
#     url = QDRANT_HOST,
#     api_key= QDRANT_API_KEY,
# )
# # create_collection
# collection_name = "rag_documents"
# vector_config = qdrant_client.http.models.VectorParams(
#     size = 4096,
#     distance = qdrant_client.http.models.Distance.COSINE
# )
# client.recreate_collection(
#     collection_name = collection_name,
#     vectors_config = vector_config,
# )

# vector_store = Qdrant(
#     client=client,
#     collection_name = collection_name,
#     embeddings=embeddings
# )
# vector_store.add_documents(texts)


qdrant = Qdrant.from_documents(
    document,
    embeddings,
    url=QDRANT_HOST,
    api_key=QDRANT_API_KEY,
    prefer_grpc=True,
    collection_name="rag_documents",
    force_recreate=True,
)
