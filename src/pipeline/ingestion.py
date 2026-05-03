from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker 
from langchain_openai import OpenAIEmbeddings
import os 
from dotenv import load_dotenv 

from src.pipeline.file_tracker import get_new_files, update_tracker
from src.rag.vector_store import add_to_vector_store, delete_vectors_by_source
from src.processing.chunking import load_and_split_documents

load_dotenv()

if os.environ.get("OPENAI_API_KEY"):
    print("OPENAI_API_KEY is set.")
else:
    raise ValueError("Brak klucza OPENAI_API_KEY w pliku .env!")




if __name__ == "__main__":
    raw_data = "data/raw"
    new_files = get_new_files(raw_data)

    if not new_files:

        print("No new documents to process")
        exit()
    
    success_list = []

    for file in new_files: 

        try:
            delete_vectors_by_source(file)
            chunks = load_and_split_documents(file)
            add_to_vector_store(chunks)
            success_list.append(file)
        except Exception as e:
            print(f"Error while processing {file} : {e}")

        
    if success_list:
        update_tracker(success_list)


    
