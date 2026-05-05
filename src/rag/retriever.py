from src.rag.vector_store import get_vector_store

def get_relevant_chunks(query: str, k: int = 5):

    db  = get_vector_store()
 
    return db.similarity_search(query, k)

