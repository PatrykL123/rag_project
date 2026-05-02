from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker 
from langchain_openai import OpenAIEmbeddings
import os 
from dotenv import load_dotenv 

load_dotenv()

if os.environ.get("OPENAI_API_KEY"):
    print("OPENAI_API_KEY is set.")
else:
    raise ValueError("Brak klucza OPENAI_API_KEY w pliku .env!")



def load_and_split_documents(file_path: str):

    document = PyPDFLoader(file_path).load()

    chunker = SemanticChunker(
        OpenAIEmbeddings(model="text-embedding-3-small"),
        breakpoint_threshold_type = "percentile",
        breakpoint_threshold_amount= 60
    )

    semantic_chunks = chunker.split_documents(document)

    return semantic_chunks


#testing 

if __name__ == "__main__":
    semantic_chunks = load_and_split_documents("data/raw/")
    print("Number of semantic chunks:", len(semantic_chunks))
    print("First 2 semantic chunks: \n")
    for i, doc in enumerate(semantic_chunks[:2]):
        print(f"chunk {i + 1}: \n {doc}")

