# For partitioning pdf
from docx import Document as Doc
from lxml import html
from pydantic import BaseModel
from typing import Any, Optional
from unstructured.partition.pdf import partition_pdf

def create_pdf_elements(pdf_filename):
    """
    A function to separate text and tables from a pdf file. This function uses
    unstructured library to convert a pdf file to a pdf image, then read
    whether a specific part is a block of text or table. It then separates the
    file into elements, which are tables and texts. 
    
    Input:
    pdf_filename: string -> The name of pdf file
    
    Output:
    raw_pdf_elements: Unstructured Partition PDF object
    """
    raw_pdf_elements = partition_pdf(filename=pdf_filename,
                                 # Unstructured first finds embedded image blocks
                                 extract_images_in_pdf=False,
                                 # Use layout model (YOLOX) to get bounding boxes (for tables) and find titles
                                 # Titles are any sub-section of the document
                                 infer_table_structure=True,
                                 # Post processing to aggregate text once we have the title
                                 chunking_strategy="by_title",
                                 # Chunking params to aggregate text blocks
                                 # Attempt to create a new chunk 3800 chars
                                 # Attempt to keep chunks > 2000 chars
                                 max_characters=2000,
                                 new_after_n_chars=1800,
                                 combine_text_under_n_chars=1000,
                                 #image_output_dir_path=path
                                 )
    return raw_pdf_elements

def separate_table_and_text(raw_pdf_elements):
    """
    A function to convert raw pdf elements into lists of texts and tables. It 
    takes an unstructured partition pdf object, then extract the elements and
    convert it into lists. 
    
    Input:
    raw_pdf_elements: Unstructured Partition PDF object
    
    Output:
    filtered_list: List -> List of all the elements in the pdf file 
    table_elements: List -> List of table elements in the pdf file. Used for converting the elements into summaries by LLM.
    text_elements: List -> List of text elements in the pdf file. Used for converting the elements into summaries by LLM.
    table_indices: List -> List of indices of the table elements. Used for recombining elements into one text
    text_indices: List -> List of indices of the text elements. Used for recombining elements into one text
    """
    class Element(BaseModel):
        type: str
        text: Any
    categorized_elements = []
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
            categorized_elements.append(Element(type="table", text=str(element)))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
            categorized_elements.append(Element(type="text", text=str(element)))

    # Discarding empty text values and save it to filtered_list
    filtered_list = [i for i in categorized_elements if i.text != '']
    
    # Separate table and text elements into a different list
    # Tables
    table_elements = [e for e in filtered_list if e.type == "table"]
    # Texts
    text_elements = [e for e in filtered_list if e.type == "text"]

    # Extract Indices from the filtered_list for table and text elements
    # to be used to reconstruct summaries into a list in the correct order
    table_indices = [i for i, e in enumerate(filtered_list) if e in table_elements]
    text_indices = [i for i, e in enumerate(filtered_list) if e in text_elements]

    return filtered_list, table_elements, text_elements, table_indices, text_indices

def recombine_elements(categorized_elements, table_summaries, text_summaries, table_indices, text_indices):
    """
    A function to recombine text and table elements into a list.
    This function takes the summaries and recombine it into the correct order
    based on the categorized_elements, table_indices, and text_indices gained
    from separate_table_and_text function.
    
    Input:
    categorezed_elements: List -> List of all the elements in the pdf file
    table_summaries: List -> List of table summaries done by LLM
    text_summaries: List -> List of text summaries done by LLM
    table_indices: List -> List of indices of the table elements    
    text_indices: List -> List of indices of the text elements

    Output:
    combined_elements -> List of combined summaries in the correct order
    """
    combined_elements = []
    for i in range(len(categorized_elements)):
        if i in table_indices:
            combined_elements.append(table_summaries[table_indices.index(i)])
        elif i in text_indices:
            combined_elements.append(text_summaries[text_indices.index(i)])
    return combined_elements

def create_docx(docx_dir, combined_elements, pdf_filename):
    """
    A function to save combined elements to docx
    
    Input:
    docx_dir: The directory where the .docx will be saved
    combined_elements: a list of combined text and table elements from recombine_elements function
    pdf_filename: the pdf filename, to be used as the name of the .docx
    """
    
    # Create a new Document
    doc = Doc()

    # Add text to the Document
    for text in combined_elements:
        doc.add_paragraph(text)

    # Save the DOCX file
    docx_filename = docx_dir + pdf_filename.replace('.pdf', '.docx')
    doc.save(docx_filename)

    print(f"DOCX file '{docx_filename}' created successfully.")