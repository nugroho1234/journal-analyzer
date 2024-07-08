# Prompt for table data
prompt_table="""You are an expert researcher with vast knowledge of quantitative and qualitative research. \
You will be given a table from a journal article, and you will need to summarize the table so that it is easier to read. \
Create multiple paragraphs only if neccessary so that the summary is easier to read. \

Table: {element} """

# Prompt for master article
master_article_prompt = """
    \n\nAnswer the user query using the article above. \n{format_instructions}\n{query}\n\n 
    Return only the JSON, don't add anything else besides the JSON. 
"""

# Prompt for getting variable definition
beginning_definition_prompt = """
    You are an expert researcher with vast knowledge of quantitative and qualitative research. \
    Based on the context provided, please give the definition of this variable.  
"""

ending_definition_prompt = """
    Answer only using the context provided below. If you don't get any context, answer with '-'.
    Do not say 'Based on the context provided, ...'. Just answer directly with the variable or concept definition.

    Context: {context}
    Question: {question}
"""