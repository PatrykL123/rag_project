from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.rag.retriever import get_relevant_chunks

def generate_answer(query: str):

    
    chunks = get_relevant_chunks(query)

    chunks_content = "\n".join([chunk.page_content for chunk in chunks])

    llm = ChatOpenAI(model = "gpt-5-mini")

    prompt = ChatPromptTemplate.from_messages(
        [
        ("system", "You are a helpful HR assistant. Answer the question based on the context below. If you don't know the answer, simply say you don't know."),
        ("user", "context :\n {chunks_content}\n\nQuery: {query}")
        ]
    )

    chain = prompt | llm 

    response = chain.invoke(
        {
        "chunks_content": chunks_content,
        "query": query
        }
    )

    return response.content





