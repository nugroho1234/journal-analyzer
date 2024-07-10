from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

master_article_query = "Get the details of this article."
quantitative_article_query = "Help me get the variables of this quantitative research article."
qualitative_article_query = "Help me get the concepts used in this qualitative research article"

class MasterArticle(BaseModel):
    title:str = Field(description="The title of this article. Typically found at the beginning of the article.")
    journal_name:str = Field(description="The name of the journal in which this article is published.")
    year_of_publication:str = Field(description="The year of publication of this article.")
    author:str = Field(description="The author(s) of this article.")
    citation:str = Field(description="How to cite this journal in APA style. Place <i></i> tag where the text should be italic")
    research_type:str = Field(description="Whether this article uses quantitative, qualitative, or other research methods. Answer with 'quantitative', 'qualitative' or 'other'.")
    summary:str = Field(description="The summary of this article. Include the research background, novelty, research gap, variables or concepts, research method, and results.")
    research_background:str = Field(description="The summary of research background in the article. It should be less than 500 words.")
    novelty:str = Field(description="The novelty of this research. If it's not mentioned, just answer with '-'.")
    research_gap:str = Field(description="The research gap of this research. If it's not mentiond, just answer with '-'.")
    sample:str = Field(description="The sample or informants used in this research. Please give the number of sample used and who they are. Example: 200 university students.")
    research_method:str = Field(description="The method used in this research.")
    results:str = Field(description="The summary of the results of this research.")
    limitations:str = Field(description="The limitations of this research. Answer with '-' if not mentioned.")
    future_research:str = Field(description="The future research directions proposed by the researcher(s). Answer with '-' if not mentioned.")

class QuantitativeArticle(BaseModel):
    independent_var:List = Field(description="A list of independent variables used in this research.")
    dependent_var:List = Field(description="A list of dependent variables used in this research. If there is none, just return an empty list.")
    mediating_var:List = Field(description="A list of mediating variables used in this research. If there is none, just return an empty list.")
    moderating_var:List = Field(description="A list of moderating variables used in this research. If there is none, just return an empty list.")
    hypothesis:str = Field(description="The hypothesis of this research. Separate each hypothesis using line break. Use numbering. For example: 1. H1: Service Quality affects customer satisfaction significantly. 2. Price affects customer satisfaction significantly. 3. Product quality affects customer satisfaction significantly. If there is no hypothesis, return '-'.")
    hypothesis_results:str = Field(description="The result of the hypothesis testing. Separate each hypothesis using line break. Use numbering. For example: 1. Service Quality affects customer satisfaction significantly. Therefore, H1 is supported. 2. Price does not affect customer satisfaction significantly. Therefore, H2 is not supported. 3. Product quality affects customer satisfaction significantly. Therefore, H3 is supported. If there is no hypothesis, return '-'.")

class QualitativeArticle(BaseModel):
    concepts:List = Field(description="A list of the concepts explored in this research.")