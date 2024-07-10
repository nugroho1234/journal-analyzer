# Insert the dictionary into the table
insert_query_master_article = """
INSERT INTO master_article (
    article_id, title, journal_name, year_of_publication, author, citation, research_type,
    summary, file_name
) VALUES %s
"""

insert_query_quantitative_articles = """
INSERT INTO quantitative_articles (
    article_id, research_background, novelty, research_gap, 
    independent_var, dependent_var, mediating_var, moderating_var,
    hypothesis, sample, research_method, results, limitations, future_research
) VALUES %s
"""

insert_query_qualitative_articles = """
INSERT INTO qualitative_articles (
    article_id, research_background, novelty, research_gap, 
    sample, concepts,
    research_method, results, limitations, future_research
) VALUES %s
"""

insert_query_master_concept = """
INSERT INTO master_concept (
    concept_id, name, type
) VALUES %s
"""

insert_query_definitions = """
INSERT INTO definitions (
    def_id, name, concept_id, article_id, definition
) VALUES %s
"""

