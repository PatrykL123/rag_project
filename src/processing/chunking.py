from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker 
from langchain_openai import OpenAIEmbeddings

def load_and_split_documents(file_path: str):
    document = PyPDFLoader(file_path).load()

    chunker = SemanticChunker(
        OpenAIEmbeddings(model="text-embedding-3-small"),
        breakpoint_threshold_type="percentile",
        breakpoint_threshold_amount=60
    )

    return chunker.split_documents(document)