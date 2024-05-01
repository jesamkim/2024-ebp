from langchain_community.document_loaders import PDFPlumberLoader
from os import listdir
from os.path import isfile, join


def get_file_list(dirpath):
    return [f for f in listdir(dirpath) if isfile(join(dirpath, f))]


def get_docs(filepath):
    loader = PDFPlumberLoader(filepath)
    return loader.load()

def get_merged_contents(filepath):
    loader = PDFPlumberLoader(filepath)
    docs = loader.load()
    page_content = ""
    for i in range(0, len(docs)):
        page_content = page_content + docs[i].page_content
    return page_content

def get_merged_page_contents(file_path: str, number: int):
    loader = PDFPlumberLoader(file_path)
    docs = loader.load()

    result = []
    for i in range(0, len(docs), number):
        page_content = ''
        for j in range(number):
            if i + j < len(docs):
                page_content = page_content + docs[i + j].page_content
        docs[i].page_content = page_content
        result.append(docs[i])
    return result
