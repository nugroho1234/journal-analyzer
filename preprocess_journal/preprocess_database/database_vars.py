from langchain_core.pydantic_v1 import BaseModel, Field

master_article_query = "Get the details of this article."

class MasterArticle(BaseModel):
    title:str = Field(description="The title of this article. Typically found at the beginning of the article,")
    journal_name:str = Field(description="The name of the journal in which this article is published")
    year_of_publication:str = Field(description="The year of publication of this article")
    author:str = Field(description="The author(s) of this article")
    citation:str = Field(description="How to cite this journal in APA style. Place <i></i> tag where the text should be italic")
    research_type:str = Field(description="Whether this article uses quantitative, qualitative, or other research methods. Answer with 'quantitative', 'qualitative' or 'other'.")
    summary:str = Field(description="The summary of this article. Include the research background, novelty, research gap, variables or concepts, research method, and results")
