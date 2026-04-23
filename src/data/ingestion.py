from langchain_community.document_loaders import PyPDFDirectoryLoader 
from langchain_experimental.text_splitter import SemanticChunker 
from langchain_openai import OpenAI, OpenAIEmbeddings
import os 
from dotenv import load_dotenv 

load_dotenv()

if os.environ.get("OPENAI_API_KEY"):
    print("OPENAI_API_KEY is set.")
else:
    raise ValueError("Brak klucza OPENAI_API_KEY w pliku .env!")


# Load the PDF documents

documents = PyPDFDirectoryLoader("data/raw/", glob="**/*.pdf").load()


# creating semantic chunks

chunker = SemanticChunker(
    OpenAIEmbeddings(model="text-embedding-3-small"),
    breakpoint_threshold_type = "percentile",
    breakpoint_threshold_amount = 60
)
 
semantic_chunks = chunker.split_documents(documents)


#testing 

if __name__ == "__main__":
    print("Number of semantic chunks:", len(semantic_chunks))
    print("First 2 semantic chunks: \n")
    for i, doc in enumerate(semantic_chunks[:2]):
        print(f"chunk {i + 1}: \n {doc.page_content}")

