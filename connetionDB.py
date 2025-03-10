# db.py
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_qdrant import QdrantVectorStore


def get_qdrant_client():
    load_dotenv()
    return QdrantClient(
        url=os.getenv("URL_BD_VECTOR"),
        api_key=os.getenv("BD_VECTOR"),
        https=True,
        timeout=300
    )


def connected_db():
    client = get_qdrant_client()
    print(client.get_collections())  # Para verificar
    return QdrantVectorStore(
        client=client,
        collection_name="laive",
        embedding=OpenAIEmbeddings(model="text-embedding-ada-002"),
    )
