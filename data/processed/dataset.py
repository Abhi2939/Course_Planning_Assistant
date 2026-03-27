from langchain_core.documents import Document
import re

def extract_course_id(text):
    match = re.search(r'COURSE_ID:\s*(CS \d+)', text)
    return match.group(1) if match else "unknown"

with open("data/raw/courses.txt","r",encoding="utf-8") as f:
    text = f.read()

docs = text.split("==================================================")

documents = []

for doc in docs:
    if doc.strip() == "":
        continue

    documents.append(
        Document(
            page_content = doc,
            metadata = {
                "source":"catalog",
                "course_id": extract_course_id(doc)
                }
        )
    )