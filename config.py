import os

# directories and paths
CURRENT_DIR = os.getcwd()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PROJECT_DIR = os.path.dirname(PARENT_DIR)

# vectorstores config
VECTOR_DIR = 'vectorstores'
MASTER_ARTICLE_DB = 'master-article'
SUMMARY_DB = 'article-summary'
VECTORSTORES = os.path.join(CURRENT_DIR, VECTOR_DIR)
MASTER_ARTICLE_CHROMA_PATH = os.path.join(VECTORSTORES, MASTER_ARTICLE_DB)
ARTICLE_SUMMARY_CHROMA_PATH = os.path.join(VECTORSTORES, SUMMARY_DB)

# gcs config
BUCKET_NAME = 'journal_analyzer_bucket'