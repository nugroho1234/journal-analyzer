import config
from preprocess_journal.article_tools.preprocess_article import process_article
from preprocess_journal.preprocess_database.data_extraction import (
    extract_master_article_details
)
from preprocess_journal.preprocess_database.database_vars import (
    MasterArticle,
    master_article_query
)
from preprocess_journal.tools import generate_random_string
from prompts import (
    prompt_table,
    master_article_prompt
)

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from dotenv import load_dotenv
import os
from typing import List, Tuple

load_dotenv()

# environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key

# vectorstores directories
MASTER_ARTICLE_PATH = config.MASTER_ARTICLE_CHROMA_PATH
ARTICLE_SUMMARY_PATH = config.ARTICLE_SUMMARY_CHROMA_PATH

# LLMs
model = ChatOpenAI(temperature=0,model="gpt-4o")
embeddings = HuggingFaceEmbeddings(model_name='intfloat/multilingual-e5-base',
                                    model_kwargs={'device': 'cpu'})
llm = ChatAnthropic(temperature=0,model="claude-3-haiku-20240307")
# prompts
prompt_table_template = PromptTemplate(input_variables=["element"], template=prompt_table)

# file
file_1 = "notebook/1-layout.pdf"


# preprocessing PDFs
combined_elements, big_context = process_article(file_1, prompt_table_template, model)

# get article details
master_article_parser = JsonOutputParser(pydantic_object=MasterArticle)

master_article_details = extract_master_article_details(big_context,
                                                 master_article_prompt,
                                                 master_article_parser,
                                                 llm,
                                                 master_article_query
                                                 )
print(master_article_details)

'''
prompt_template_ending = """
    \n\nAnswer the user query using the article above. \n{format_instructions}\n{query}\n\n 
"""

prompt = PromptTemplate(
    template = big_context + prompt_template_ending,
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

llm = ChatAnthropic(temperature=0,model="claude-3-haiku-20240307")

chain = prompt | llm | parser

results = chain.invoke({"query": master_article_query})
print(dict(results))
'''
'''
# master article embeddings 
collection_name = 'master_article_embeddings'
article_id = generate_random_string('ART')
metadata_dict = {}
metadata_dict['article_id'] = article_id
combined_docs = [Document(page_content=i, metadata = metadata_dict) for i in combined_elements]

db = Chroma.from_documents(combined_docs, embeddings, persist_directory=MASTER_ARTICLE_PATH)
db.persist()

llm = ChatOpenAI(temperature=0,model="gpt-3.5-turbo-1106")
db = Chroma(persist_directory=MASTER_ARTICLE_PATH, embedding_function=embeddings)


results = db.similarity_search('What is the title of this article?', k=1)
context = results[0].page_content
PROMPT_TEMPLATE = """You are an expert in understanding journal articles. 
You will be asked about the variables used of a journal article. 
Answer the question based on the context provided only.
Answer the question by just the variables of the article only.
If you cannot find the context, just say that you don't know.

Context: {context}
Question: {question}
"""
prompt = PromptTemplate(template=PROMPT_TEMPLATE, 
                        input_variables=['context','question'],

                        )

query = 'What are the dependent variables used in this article?'
qa_chain = RetrievalQA.from_chain_type(
            llm = llm,
            chain_type = 'stuff',
            retriever = db.as_retriever(search_kwargs={'k':10}),
            return_source_documents = True,
            chain_type_kwargs = {'prompt':prompt}
        )

response = qa_chain.invoke({'query':query})
print(response['result'])
'''
