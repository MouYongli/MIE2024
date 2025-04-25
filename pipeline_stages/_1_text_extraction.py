import re

import docx2txt
import PyPDF2
from docx import Document


def read_pdf(file_path: str):
    """
    Get the content of a pdf document.

    Args:
        file_path (str): path to the pdf file

    Returns:
        str: content of the pdf file
    """
    with open(file_path, "rb") as file:
        pdf = PyPDF2.PdfReader(file)
        content = ""
        for page in pdf.pages:
            content += page.extract_text()
    return content


def read_docx_2(file_path: str):
    """
    Get the content of a docx document.

    Args:
        file_path (str): path to the docx file

    Returns:
        str: content of the docx file
    """
    doc = Document(file_path)
    paragraphs = []
    for p in doc.paragraphs:
        # if p.text.strip() != "":
        paragraphs.append(p.text)
    content = "\n".join(paragraphs)
    # content = re.sub("\n\s*\n", "\n\n", content)

    return content


def read_docx(file_path: str):
    """
    Get the content of a docx document.

    Args:
        file_path (str): path to the docx file

    Returns:
        str: content of the docx file
    """
    content = docx2txt.process(file_path)
    content = re.sub("\n\s*\n", "\n", content)

    return content


def read_all_docxs(file_paths: list):
    """
    Get the content of multiple docx documents

    Args:
        file_paths (list): list of paths to the docx files

    Returns:
        dict: dictionary with the contents of the docx files
        as values and 'Dokument {index+1}' as keys
    """
    content_dict = {}
    for index, file_path in enumerate(file_paths):
        content = read_docx_2(file_path)
        content_dict[f"Dokument {index+1}"] = content
    return content_dict
