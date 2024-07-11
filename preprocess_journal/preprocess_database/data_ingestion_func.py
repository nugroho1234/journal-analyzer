import psycopg2
from psycopg2.extras import execute_values
from typing import Any

def checker_name_exists(conn, table_name: str, column_name: str, concept_name: str) -> bool:
    with conn.cursor() as cur:
        cur.execute(f"SELECT 1 FROM {table_name} WHERE {column_name} = %s LIMIT 1;", (concept_name,))
        return cur.fetchone() is not None

def get_concept_id(conn, table_name: str, column_name: str, concept_name: str) -> int:
    with conn.cursor() as cur:
        cur.execute(f"SELECT concept_id FROM {table_name} WHERE {column_name} = %s;", (concept_name,))
        result = cur.fetchone()
        return result[0] if result else None
    
def ingest_to_master_article(cur: Any,
                             insert_query_master_article:str,
                             article_id:str,
                             title:str,
                             journal_name:str,
                             year_of_publication:str,
                             author:str,
                             citation:str,
                             research_type:str,
                             summary:str,
                             file_name:str):
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

def ingest_quantitative(cur:Any,
                        insert_query_quantitative_articles:str,
                        article_id:str,
                        research_background:str,
                        novelty:str,
                        research_gap:str,
                        independent_vars:str,
                        dependent_vars:str,
                        mediating_vars:str,
                        moderating_vars:str,
                        hypothesis:str,
                        sample:str,
                        research_method:str,
                        results:str,
                        limitations:str,
                        future_research:str):
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

def ingest_qualitative(cur:Any,
                       insert_query_qualitative_articles:str,
                       article_id:str,
                       research_background:str,
                       novelty:str,
                       research_gap:str,
                       sample:str,
                       concepts:str,
                       research_method:str,
                       results:str,
                       limitations:str,
                       future_research:str):
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

def ingest_master_concept(cur:Any,
                          insert_query_master_concept:str,
                          concept_id:str,
                          concept_name:str,
                          concept_type:str):
    values = (
                concept_id,
                concept_name,
                concept_type
            )
            
    execute_values(cur, insert_query_master_concept, [values])

def ingest_definitions(cur:Any,
                       insert_query_definitions:str,
                       def_id:str,
                       concept_name:str,
                       concept_id:str,
                       article_id:str,
                       concept_definition:str):
    values = (
                def_id,
                concept_name,
                concept_id,
                article_id,
                concept_definition
            )

    execute_values(cur, insert_query_definitions, [values])