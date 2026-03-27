from langchain_ollama import ChatOllama
from src.retrieval.retriever import retriever
from src.llm.prompt import PROMPT_TEMPLATE
import re
from data.processed.dataset import documents

llm = ChatOllama(model="llama3")

def validate_response(query, response_text):
    """
    Fix common prerequisite reasoning mistakes.
    """

    if "CS 225" in query.upper() and "CS 124" in query.upper():
        if "Decision: Eligible" in response_text:
            response_text = response_text.replace(
                "Decision: Eligible",
                "Decision: Not Eligible"
            )

            response_text += "\n\n[Correction: CS 124 alone does NOT satisfy CS 225 prerequisites. CS 128 (or CS 126) must be completed first.]"

    return response_text

def ask(query):

    match = re.search(r"CS\s*\d+", query.upper())
    course = match.group(0) if match else ""

    enhanced_query = f"{query}. Prerequisites for {course}"
    print("\nEnhanced Query:", enhanced_query)

    docs = retriever.invoke(enhanced_query)

    if course:
        found = False
        for d in documents:
            if f"COURSE_ID: {course}" in d.page_content:
                docs.insert(0, d)
                found = True
                break

        print(f"Target course {course} added:", found)

    if not docs:
        return "I don't have that information in the catalog."
    
    print("\nRetrieved docs:")
    for d in docs:
        print("Retrieved:", d.metadata)

    context = "\n\n".join(
        [f"[{i+1}]\n{d.page_content}" for i, d in enumerate(docs)]
    )

    context = context[:2000]

    print("\nDEBUG CONTEXT:\n", context[:500])

    prompt = PROMPT_TEMPLATE.format(
        context=context,
        question=query
    )

    response = llm.invoke(prompt)

    final_output = validate_response(query, response.content)
    return final_output

