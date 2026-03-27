from langchain_ollama import ChatOllama
from src.retrieval.retriever import retriever
from src.llm.prompt import PROMPT_TEMPLATE

llm = ChatOllama(model = "llama3")

def ask(query):

    docs = retriever.invoke(query)

    context = "\n\n".join([d.page_content for d in docs])

    prompt = PROMPT_TEMPLATE.format(
        context=context,
        question=query
    )

    response = llm.invoke(prompt)

    return response.content