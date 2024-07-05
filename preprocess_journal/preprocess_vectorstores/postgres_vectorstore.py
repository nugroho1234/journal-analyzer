from langchain_core import document_loaders
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGEmb

'''
connection = "postgresql://agusnug:danifiltH7!1985@localhost:5432/journal_analyzer_database"
collection_name = "vector_summary"
embeddings = HuggingFaceEmbeddings(model_name='intfloat/multilingual-e5-base',
                                model_kwargs={'device': 'cpu'})
'''

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