def create_big_summary_opening(title: str,
                               research_background: str,
                               novelty: str,
                               research_gap: str,
                               research_type: str,
                               research_method: str,
                               sample: str):
    
    novelty_summary = ''
    gap_summary = ''
    #create big summary

    background_summary = f'The title of this research is {title} and the research background is as follows: \n{research_background}\n\n'
    if novelty != '-':
        novelty_summary = f'The novelty of this research is: \n{novelty}\n\n'
    if research_gap != '-':
        gap_summary = f'The research gap of this article is: \n{research_gap}\n\n'
    method_summary = f'This is a {research_type} research using the method: \n{research_method}\n\n'
    sample_summary = f'The sample used in this research is: \n{sample}\n\n'

    big_summary = background_summary + novelty_summary + gap_summary + method_summary + sample_summary
    return big_summary

def create_quantitative_summary(independent_vars: str,
                                dependent_vars: str,
                                mediating_vars: str,
                                moderating_vars: str,
                                hypothesis: str):
    independent_var_summary = ''
    dependent_var_summary = ''
    mediating_var_summary = ''
    moderating_var_summary = ''
    hypothesis_summary = ''

    independent_var_summary = f'The independent variables used in this research: {independent_vars}\n\n'
    if len(dependent_vars) > 0:
        dependent_var_summary = f'The dependent variables used in this research: {dependent_vars}\n\n'
    if len(mediating_vars) > 0:
        mediating_var_summary = f'The mediating variables used in this research: {mediating_vars}\n\n'
    if len(moderating_vars) > 0:
        moderating_var_summary = f'The moderating variables used in this research: {moderating_vars}\n\n'
    if hypothesis != '-':
        hypothesis_summary = f'The hypothesis of this research: \n{hypothesis}\n\n'
    
    quantitative_summary = independent_var_summary + dependent_var_summary + mediating_var_summary + moderating_var_summary + hypothesis_summary

    return quantitative_summary

def create_qualitative_summary(concepts:str):
    concepts_summary = ''
    concepts_summary = f'The concepts used in this research: {concepts}\n\n.'
    return concepts_summary

def create_big_summary_ending(results: str):
    results_summary = ''
    results_summary = f'The results of this research are: \n{results}\n\n'
    return results_summary