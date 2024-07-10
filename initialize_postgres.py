from preprocess_journal.preprocess_database.table_creation_func import (
    check_and_create_table,
    create_index,
    delete_table,
    print_table_names
)

from dotenv import load_dotenv
import os

# confidential info
load_dotenv()
dbname = os.getenv('POSTGRES_DBNAME')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = 'localhost'

# queries
# master_table query
master_article_query = '''
CREATE TABLE master_article (
    article_id CHAR(16) PRIMARY KEY,
    title TEXT,
    journal_name TEXT,
    year_of_publication INT CHECK (year_of_publication >= 1000 AND year_of_publication <= 9999),
    author TEXT,
    citation TEXT,
    research_type TEXT,
    summary TEXT,
    file_name TEXT
);
'''

master_concept_query = '''
CREATE TABLE master_concept (
    concept_id CHAR(16) PRIMARY KEY,
    name TEXT,
    type TEXT
);
'''

quantitative_articles_query = """
CREATE TABLE quantitative_articles (
    article_id CHAR(16) PRIMARY KEY REFERENCES master_article(article_id),
    research_background TEXT,
    novelty TEXT,
    research_gap TEXT,
    independent_var TEXT,
    dependent_var TEXT,
    mediating_var TEXT,
    moderating_var TEXT,
    hypothesis TEXT,
    sample TEXT,
    research_method TEXT,
    results TEXT,
    limitations TEXT,
    future_research TEXT
);
"""

qualitative_articles_query = """
CREATE TABLE qualitative_articles (
    article_id CHAR(16) PRIMARY KEY REFERENCES master_article(article_id),
    research_background TEXT,
    novelty TEXT,
    research_gap TEXT,
    concepts TEXT,
    hypothesis TEXT,
    sample TEXT,
    research_method TEXT,
    results TEXT,
    limitations TEXT,
    future_research TEXT
);
"""

definitions_query = """
CREATE TABLE definitions (
    def_id CHAR(16) PRIMARY KEY,
    name TEXT,
    concept_id CHAR(16) REFERENCES master_concept (concept_id), 
    article_id CHAR(16) REFERENCES master_article (article_id), 
    definition TEXT
);
"""
'''
# DELETING TABLES
delete_table(dbname, user, password, host, 'master_article')
delete_table(dbname, user, password, host, 'master_concept')
delete_table(dbname, user, password, host, 'quantitative_articles')
delete_table(dbname, user, password, host, 'definitions')

'''

# CREATING TABLES
check_and_create_table(dbname, user, password, host, 'master_article', master_article_query)
check_and_create_table(dbname, user, password, host, 'master_concept', master_concept_query)
check_and_create_table(dbname, user, password, host, 'quantitative_articles', quantitative_articles_query)
check_and_create_table(dbname, user, password, host, 'qualitative_articles', qualitative_articles_query)
check_and_create_table(dbname, user, password, host, 'definitions', definitions_query)
create_index(dbname, user, password, host)

print_table_names(dbname, user, password, host)
