from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate

def extract_master_article_details(big_context:str, 
                            prompt_template_ending:str,
                            parser:JsonOutputParser,
                            llm:ChatAnthropic,
                            master_article_query:str):
    
    prompt = PromptTemplate(
        template = big_context + prompt_template_ending,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = prompt | llm | parser
    results = chain.invoke({"query": master_article_query})        
    return dict(results)
