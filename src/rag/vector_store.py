from src.data.ingestion import load_and_split_documents 
from langchain_community.vectorstores import Chroma 
from langchain_openai import OpenAIEmbeddings


def add_to_vector_store(semantic_chunks):

    db = get_vector_store()

    db.add_documents(documents = semantic_chunks)


def get_vector_store():

    return Chroma(persist_directory = "data/chroma_db", embedding_function = OpenAIEmbeddings(model="text-embedding-3-small"))

    

def delete_vectors_by_source(file_path: str):

    db = get_vector_store()

    vectors = db.get(where = {"source" : file_path})

    ids_to_delete = vectors.get("ids", [])

    if ids_to_delete:

        db.delete(ids = ids_to_delete)

        print(f"Deleted {len(ids_to_delete)} old chunks from Database")
    else: 

        print("No old chunkd to delete (it's new file)")

