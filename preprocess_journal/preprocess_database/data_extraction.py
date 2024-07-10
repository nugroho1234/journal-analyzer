from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import PromptTemplate

def extract_master_article_details(big_context:str, 
                            prompt_template_ending:str,
                            parser:JsonOutputParser,
                            llm:ChatAnthropic,
                            master_article_query:str):
    big_context = big_context.replace("{", "{{").replace("}", "}}")
    #prompt_template_ending = prompt_template_ending.replace("{", "{{").replace("}", "}}")
    print(big_context)
    print(prompt_template_ending)
    prompt = PromptTemplate(
        template = big_context + prompt_template_ending,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = prompt | llm | parser
    results = chain.invoke({"query": master_article_query})
    print(results)        
    return dict(results)

def extract_variables(big_context:str,
                      prompt_template_ending:str,
                      parser:JsonOutputParser,
                      llm:ChatAnthropic,
                      quantitative_article_query:str):
    big_context = big_context.replace("{", "{{").replace("}", "}}")
    #prompt_template_ending = prompt_template_ending.replace("{", "{{").replace("}", "}}")
    prompt = PromptTemplate(
        template = big_context + prompt_template_ending,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = prompt | llm | parser
    results = chain.invoke({"query": quantitative_article_query})        
    return dict(results)

def extract_concepts(big_context:str,
                     prompt_template_ending:str,
                     parser:JsonOutputParser,
                     llm:ChatAnthropic,
                     qualitative_article_query:str):
    big_context = big_context.replace("{", "{{").replace("}", "}}")
    #prompt_template_ending = prompt_template_ending.replace("{", "{{").replace("}", "}}")
    prompt = PromptTemplate(
        template = big_context + prompt_template_ending,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = prompt | llm | parser
    results = chain.invoke({"query": qualitative_article_query})        
    return dict(results)
