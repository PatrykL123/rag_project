from src.data.ingestion import load_and_split_documents 
from langchain_community.vectorstores import Chroma 
from langchain_openai import OpenAIEmbeddings


def create_vector_store(semantic_chunks, persist_directory):
    # Create a Chroma vector store from the semantic chunks
    embed_model = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = Chroma.from_documents(
        documents=semantic_chunks,
        embedding=embed_model,
        persist_directory=persist_directory
    )


#testing 

if __name__ == "__main__":

    print("Loading and splitting documents...")

    chunks = load_and_split_documents("data/raw/")

    print("Number of semantic chunks:", len(chunks))

    print("Creating vector store...")
    create_vector_store(chunks, "data/chroma_db/")

    print("Vector store created")

    print("testing vector store...")

    vector_store_con = Chroma(persist_directory="data/chroma_db/", embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"))
    query = "What is the main topic of the document?"
    result = vector_store_con.similarity_search(query, k=3)
    print("Query result:\n", result)