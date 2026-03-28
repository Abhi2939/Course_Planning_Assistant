from langchain_ollama import ChatOllama
from langchain_community.vectorstores import FAISS
from src.embedding.embeddings import embeddings
#from src.retrieval.retriever import retriever
from src.llm.prompt import PROMPT_TEMPLATE
import re

db = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

llm = ChatOllama(model="llama3")

def needs_clarification(query):
    if "plan" in query.lower() and "completed" not in query.lower():
        return True
    return False

def detect_type(query):
    q = query.lower()
    if "policy" in q or "rule" in q:
        return "POLICY"
    elif "program" in q or "degree" in q:
        return "PROGRAM"
    return "COURSE"

def ask(query):

    if needs_clarification(query):
        return """
        Clarifying Questions:
        - What courses have you completed?
        - What is your major?
        - Any credit/semester constraints?
        """

    match = re.search(r"CS\s*[-:]?\s*\d+", query.upper())
    course = match.group(0).replace(" ", "") if match else ""

    enhanced_query = f"{query}. Prerequisites for {course}" if course else query
    print("\nEnhanced Query:", enhanced_query)

    doc_type = detect_type(query)

    retriever = db.as_retriever(
        search_kwargs = {
            "k":5,
            "filter":{"type":doc_type}
        }
    )


    docs = retriever.invoke(enhanced_query)

    if not docs:
        print("⚠️ No docs with filter, retrying without filter...")
        retriever = db.as_retriever(search_kwargs={"k": 5})
        docs = retriever.invoke(enhanced_query)

    if not docs:
        return "I don't have that information in the catalog."

    # if course:
    #     found = False
    #     for d in documents:
    #         if f"COURSE_ID: {course}" in d.page_content:
    #             docs.insert(0, d)
    #             found = True
    #             break

    #     print(f"Target course {course} added:", found)

    
    
    print("\nRetrieved docs:")
    for d in docs:
        print(d.metadata)

    docs = docs[:5]

    context = "\n\n".join(
        [f"[{i+1}] ({d.metadata.get('type')})\n{d.page_content}" for i, d in enumerate(docs)]
    )

    #context = context[:6000]

    print("\n🧠 Context preview:\n", context[:500])

    prompt = PROMPT_TEMPLATE.format(
        context=context,
        question=query
    )

    response = llm.invoke(prompt)

    if "[" not in response.content:
        return "I don't have enough evidence in the catalog to answer this."

    return response.content

