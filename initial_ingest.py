import config
from ingestion_queries import (
    insert_query_master_article,
    insert_query_master_concept,
    insert_query_definitions,
    insert_query_qualitative_articles,
    insert_query_quantitative_articles
)
from preprocess_journal.preprocess_database.data_ingestion_func import (
    checker_name_exists,
    get_concept_id
)
from preprocess_journal.article_tools.preprocess_article import process_article
from preprocess_journal.article_tools.article_loader import (
    get_article_files
)
from preprocess_journal.preprocess_database.data_extraction import (
    extract_master_article_details,
    extract_concepts,
    extract_variables
)
from preprocess_journal.preprocess_database.database_vars import (
    MasterArticle,
    QualitativeArticle,
    QuantitativeArticle,
    master_article_query,
    qualitative_article_query,
    quantitative_article_query
)

from preprocess_journal.preprocess_vectorstores.summary_builder import (
    create_big_summary_opening,
    create_big_summary_ending,
    create_quantitative_summary,
    create_qualitative_summary
)

from preprocess_journal.tools import generate_unique_id
from prompts import (
    prompt_table,
    master_article_prompt,
    beginning_definition_prompt,
    ending_definition_prompt
)

from google.cloud import storage
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from psycopg2.extras import execute_values
import psycopg2

from dotenv import load_dotenv
import os
from typing import List, Tuple

# confidential info
load_dotenv()
dbname = os.getenv('POSTGRES_DBNAME')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = 'localhost'

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
cur = conn.cursor()

# environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
gcs_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcs_credentials

# vectorstores directories
MASTER_ARTICLE_PATH = config.MASTER_ARTICLE_CHROMA_PATH
ARTICLE_SUMMARY_PATH = config.ARTICLE_SUMMARY_CHROMA_PATH

# gcs buckettmp
GCS_BUCKET = config.BUCKET_NAME

# gcs storage
storage_client = storage.Client()

# LLMs
model = ChatOpenAI(temperature=0,model="gpt-4o")
embeddings = HuggingFaceEmbeddings(model_name='intfloat/multilingual-e5-base',
                                    model_kwargs={'device': 'cpu'})
llm = ChatAnthropic(temperature=0,model="claude-3-haiku-20240307")
# prompts
prompt_table_template = PromptTemplate(input_variables=["element"], template=prompt_table)



article_files = get_article_files(GCS_BUCKET, storage_client)
article_files = article_files[:5]
for file_name in article_files:
    try:
        bucket = storage_client.get_bucket(GCS_BUCKET)
        blob = bucket.blob(file_name)
        path_to_tmp_file = 'tmp/' + file_name
        blob.download_to_filename(path_to_tmp_file)
        
        # preprocessing PDFs
        print('Turning PDF into TEXT...')
        combined_elements, big_context = process_article(path_to_tmp_file, prompt_table_template, model)
        
        print('Extracting article details...')
        master_article_details = None
        quantitative_article_details = None
        qualitative_article_details = None

        master_article_parser = JsonOutputParser(pydantic_object=MasterArticle)
        quantitative_article_parser = JsonOutputParser(pydantic_object=QuantitativeArticle)
        qualitative_article_parser = JsonOutputParser(pydantic_object=QualitativeArticle)

        master_article_details = extract_master_article_details(big_context,
                                                        master_article_prompt,
                                                        master_article_parser,
                                                        llm,
                                                        master_article_query
                                                        )
        #print(master_article_details)
        article_id = generate_unique_id(conn, 'master_article', 'article_id', 'ART')
        title = master_article_details['title']
        journal_name = master_article_details['journal_name']
        year_of_publication = master_article_details['year_of_publication']
        author = master_article_details['author']
        citation = master_article_details['citation']
        research_type = master_article_details['research_type']
        summary = master_article_details['summary']
        research_background = master_article_details['research_background']
        novelty = master_article_details['novelty']
        research_gap = master_article_details['research_gap']
        research_method = master_article_details['research_method']
        sample = master_article_details['sample']
        results = master_article_details['results']
        limitations = master_article_details['limitations']
        future_research = master_article_details['future_research']

        title_exists = checker_name_exists(conn, 'master_article', 'title', title)
        if title_exists:
            pass
        else:
            #create big summary
            big_summary = create_big_summary_opening(title, 
                                                    research_background, 
                                                    novelty, 
                                                    research_gap, 
                                                    research_type, 
                                                    research_method, 
                                                    sample)
        
            if research_type == 'quantitative':
                quantitative_article_details = extract_variables(big_context,
                                                                master_article_prompt,
                                                                quantitative_article_parser,
                                                                llm,
                                                                quantitative_article_query)
                
                independent_vars = ','.join(quantitative_article_details['independent_var'])
                dependent_vars = ','.join(quantitative_article_details['dependent_var'])
                mediating_vars = ','.join(quantitative_article_details['mediating_var'])
                moderating_vars = ','.join(quantitative_article_details['moderating_var'])
                hypothesis = quantitative_article_details['hypothesis']
                if hypothesis == "-":
                    results = master_article_details['results']
                else:
                    results = quantitative_article_details['hypothesis_results']

                all_concepts = quantitative_article_details['independent_var'] + quantitative_article_details['dependent_var'] + quantitative_article_details['mediating_var'] + quantitative_article_details['moderating_var']

                quantitative_summary = create_quantitative_summary(independent_vars, 
                                                                dependent_vars, 
                                                                mediating_vars, 
                                                                moderating_vars, 
                                                                hypothesis)
                big_summary = big_summary + quantitative_summary

            elif research_type == 'qualitative':
                qualitative_article_details = extract_concepts(big_context,
                                                            master_article_prompt,
                                                            qualitative_article_parser,
                                                            llm,
                                                            qualitative_article_query)
                #print(qualitative_article_details)
                concepts = ','.join(qualitative_article_details['concepts'])
                all_concepts = qualitative_article_details['concepts']
                concepts_summary = create_qualitative_summary(concepts)
                big_summary = big_summary + concepts_summary

            results_summary = create_big_summary_ending(results)
            big_summary = big_summary + results_summary

            # INGEST TO MASTER ARTICLE DATABASE
            values = (
                article_id,
                title,
                journal_name,
                year_of_publication,
                author,
                citation,
                research_type,
                summary,
                file_name
            )

            execute_values(cur, insert_query_master_article, [values])

            # INGEST INTO QUANTITATIVE OR QUALITATIVE ARTICLE DATABASE
            if research_type == 'quantitative':
                values = (
                    article_id,
                    research_background,
                    novelty,
                    research_gap,
                    independent_vars,
                    dependent_vars,
                    mediating_vars,
                    moderating_vars,
                    hypothesis,
                    sample,
                    research_method,
                    results,
                    limitations,
                    future_research
                )

                execute_values(cur, insert_query_quantitative_articles, [values])
            elif research_type == 'qualitative':
                values = (
                    article_id,
                    research_background,
                    novelty,
                    research_gap,
                    sample,
                    concepts,
                    research_method,
                    results,
                    limitations,
                    future_research
                )
                execute_values(cur, insert_query_qualitative_articles, [values])
            
            # article embeddings 
            print('Getting embeddings and saving it to vectorstores...')
            # master article
            master_db_metadata = {}
            master_db_metadata['article_id'] = article_id
            combined_docs = [Document(page_content=i, metadata = master_db_metadata) for i in combined_elements]

            master_db = Chroma.from_documents(combined_docs, embeddings, persist_directory=MASTER_ARTICLE_PATH)
            master_db.persist()

            # summary article
            summary_docs = [Document(page_content=big_summary, metadata = master_db_metadata)]

            summary_db = Chroma.from_documents(summary_docs, embeddings, persist_directory=ARTICLE_SUMMARY_PATH)
            summary_db.persist()

            # processing master concepts and definitions
            if (research_type == 'qualitative') or (research_type == 'quantitative'):
                if len(all_concepts) > 0:
                    for concept_name in all_concepts:
                        concept_exists = checker_name_exists(conn, 'master_concept', 'name', concept_name)
                        if concept_exists:
                            concept_id = get_concept_id(conn, 'master_concept', 'name', concept_name)
                        else:
                            # PROCESSING MASTER CONCEPTS
                            concept_id = generate_unique_id(conn, 'master_concept', 'concept_id', 'CON')
                            if research_type == 'quantitative':
                                concept_type = 'variable'
                            elif research_type == 'qualitative':
                                concept_type = 'concept'
                            
                            # insert to master_concept
                            values = (
                                concept_id,
                                concept_name,
                                concept_type
                            )
                            
                            execute_values(cur, insert_query_master_concept, [values])

                        # PROCESSING DEFINITIONS
                        if research_type == 'quantitative':
                            concept_prompt = beginning_definition_prompt + f'Variable: {concept_name}\n\n' + ending_definition_prompt
                            question = f'What is the definition of this variable called {concept_name}?'
                        elif research_type == 'qualitative':
                            concept_prompt = beginning_definition_prompt + f'Concept: {concept_name}\n\n' + ending_definition_prompt
                            question = f'What is the definition of this concept called {concept_name}?'
                        
                        concept_prompt_template = PromptTemplate(template = concept_prompt, input_variables = ['context','question'])
                        
                        qa_chain = RetrievalQA.from_chain_type(
                            llm=llm,
                            chain_type = 'stuff',
                            retriever = master_db.as_retriever(search_kwargs={'k':5}),
                            return_source_documents = False,
                            chain_type_kwargs = {'prompt': concept_prompt_template}
                        )

                        response = qa_chain.invoke({'query':question})
                        concept_definition = response['result']

                        def_id = generate_unique_id(conn, 'definitions', 'def_id', 'DEF')

                        values = (
                            def_id,
                            concept_name,
                            concept_id,
                            article_id,
                            concept_definition
                        )

                        execute_values(cur, insert_query_definitions, [values])
            #delete temp file
        os.remove(path_to_tmp_file)
    except Exception as e:
        bucket = storage_client.get_bucket(GCS_BUCKET)
        blob = bucket.blob(file_name)
        path_to_tmp_file = 'unfinished/' + file_name
        blob.download_to_filename(path_to_tmp_file)

conn.commit()
cur.close()
conn.close()

