import config
from preprocess_journal.article_tools.preprocess_article import (
    create_pdf_elements,
    separate_table_and_text,
    recombine_elements,
    create_docx
)
from preprocess_journal.tools import generate_random_string
from prompts import prompt_table

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os
from typing import List, Tuple

load_dotenv()

# environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = openai_api_key

# vectorstores directories
MASTER_ARTICLE_PATH = config.MASTER_ARTICLE_CHROMA_PATH
ARTICLE_SUMMARY_PATH = config.ARTICLE_SUMMARY_CHROMA_PATH

# LLMs
model = ChatOpenAI(temperature=0,model="gpt-4o")
embeddings = HuggingFaceEmbeddings(model_name='intfloat/multilingual-e5-base',
                                    model_kwargs={'device': 'cpu'})

# prompts
prompt_table_template = PromptTemplate(input_variables=["element"], template=prompt_table)

# file
file_1 = "notebook/2-layout.pdf"


# preprocessing PDFs
raw_pdf_elements = create_pdf_elements(file_1)
categorized_elements, table_elements, text_elements, table_indices, text_indices = separate_table_and_text(raw_pdf_elements)

combined_elements = []
table_summaries = []
text_summaries = []

if len(table_elements) == 0:
    for text in text_elements:
        combined_elements.append(text.text)
else:
    tables = [i.text for i in table_elements]
    chain_table = prompt_table_template | model
    for table in tables:
        response = chain_table.invoke({
            "element": table
        })
        table_summaries.append(response.content)
    texts = [i.text for i in text_elements]
    for text in texts:
        text_summaries.append(text)
    combined_elements = recombine_elements(categorized_elements, table_summaries, text_summaries, table_indices, text_indices)

big_context = '\n'.join(combined_elements)

class MasterArticle(BaseModel):
    title:str = Field(description="The title of this article. Typically found at the beginning of the article,")
    journal_name:str = Field(description="The name of the journal in which this article is published")
    year_of_publication:str = Field(description="The year of publication of this article")
    author:str = Field(description="The author(s) of this article")
    citation:str = Field(description="How to cite this journal in APA style. Place <i></i> tag where the text should be italic")
    research_type:str = Field(description="Whether this article uses quantitative, qualitative, or other research methods. Answer with 'quantitative', 'qualitative' or 'other'.")
    summary:str = Field(description="The summary of this article. Include the research background, novelty, research gap, variables or concepts, research method, and results")

master_article_query = "Get the details of this article."

parser = JsonOutputParser(pydantic_object=MasterArticle)

prompt_template_ending = """
    \n\nAnswer the user query using the article above. \n{format_instructions}\n{query}\n\n 
"""

prompt = PromptTemplate(
    template = big_context + prompt_template_ending,
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain = prompt | model | parser

results = chain.invoke({"query": master_article_query})
print(results)

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
