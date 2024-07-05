from preprocess_journal.article_tools.preprocess_article import (
    create_pdf_elements,
    separate_table_and_text,
    recombine_elements,
    create_docx
)
from preprocess_journal.tools import generate_random_string
from prompts import prompt_table

from langchain_community.vectorstores import PGEmbedding
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

load_dotenv()

postgres_connection = os.getenv('POSTGRES_CONNECTION')
openai_api_key = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = openai_api_key

model = ChatOpenAI(temperature=0,model="gpt-4o")
prompt_table_template = PromptTemplate(input_variables=["element"], template=prompt_table)

file_1 = "notebook/2-layout.pdf"

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

journal_id = generate_random_string()
combined_docs = [Document(page_content=i, )]