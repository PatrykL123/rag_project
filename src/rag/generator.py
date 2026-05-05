from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.rag.retriever import get_retriever


def format_chunks(chunks):
      
    return "\n".join([chunk.page_content for chunk in chunks])


def generate_answer(query: str, chat_history: list):

    llm_question_builder = ChatOpenAI(model = "gpt-4o-mini")
    llm = ChatOpenAI(model = "gpt-5-mini", temperature = 0)
    retriever = get_retriever()


    context_prompt = ChatPromptTemplate.from_messages(
        [
        ("system", """Given a chat history and the latest user question.
         which might reference context in the chat history, 
         formulate a standalone question which can be understood
         without the chat history. Do NOT answer the question, 
         just reformulate it if needed and otherwise return it as is."""),
        MessagesPlaceholder("chat_history"),
        ("user", "Query: {query}")
        ]
    )

    history_aware_retriever = (
        context_prompt 
        | llm_question_builder
        | StrOutputParser()
        | retriever 
        | format_chunks
    )


    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", ("""
            You are a helpful assistant. Answer the question based on the context below.
            If you don't know the answer, simply say you don't know.\n\n
            Context:\n{context}
        """)),
        MessagesPlaceholder("chat_history"),
        ("user", "{query}")

    ])


    rag_chain = (

        RunnablePassthrough.assign(context = history_aware_retriever)
        | qa_prompt
        | llm
        |StrOutputParser()
    )

    response = rag_chain.invoke(
        {
        "query": query,
        "chat_history": chat_history
        }
    )

    return response





