# Prompt for table data
prompt_table="""You are an expert researcher with vast knowledge of quantitative and qualitative research. \
You will be given a table from a journal article, and you will need to summarize the table so that it is easier to read. \
Create multiple paragraphs only if neccessary so that the summary is easier to read. \

Table: {element} """

# Prompt for master article
master_article_prompt = """
    \n\nAnswer the user query using the article above. \n{format_instructions}\n{query}\n\n 
"""