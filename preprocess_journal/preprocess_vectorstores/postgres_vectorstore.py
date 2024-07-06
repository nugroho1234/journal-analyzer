from langchain_core import document_loaders
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGEmb

def create_postgres_vectorstore(connection: str,
                                collection_name: str,
                                embeddings: HuggingFaceEmbeddings):

    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=connection,
        use_jsonb=True
    )
    return vectorstore