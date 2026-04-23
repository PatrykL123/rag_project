from langchain_community.document_loaders import PyPDFLoader 
from langchain_experimental.text_splitter import SemanticChunker 
from langchain_openai import OpenAI, OpenAIEmbeddings
import os 
from dotenv import load_dotenv 

load_dotenv()

if os.environ.get("OPENAI_API_KEY"):
    print("OPENAI_API_KEY is set.")
else:
    print("OPENAI_API_KEY is not set. Please set it in the .env file.")


# Load the PDF document

documents = PyPDFLoader("data/raw/HR_documents.pdf").load()

# changing document into text 

full_text = "\n".join([page.page_content for page in documents])

# creating semantic chunks

chunker = SemanticChunker(
    OpenAIEmbeddings(model="text-embedding-3-small"),
    breakpoint_threshold_type = "percentile",
    breakpoint_threshold_amount = 60
)
 
semantic_chunks = chunker.create_documents([full_text])
