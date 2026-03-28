from langchain_core.documents import Document
import re


def extract_field(pattern, text, default=""):
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else default


def build_page_content(doc):
    doc_type = extract_field(r"TYPE:\s*(.*)", doc)
    title = extract_field(r"TITLE:\s*(.*)", doc)

    if doc_type == "COURSE":
        description = extract_field(r"DESCRIPTION:\n(.*?)\n\nPREREQUISITES:", doc)
        prereq = extract_field(r"PREREQUISITES:\n(.*?)\n\nSOURCE:", doc)

        return f"""Course: {title}

Description:
{description}

Prerequisites:
{prereq}
"""

    else:  # PROGRAM / POLICY
        content = extract_field(r"CONTENT:\n(.*?)\n\nSOURCE:", doc)

        return f"""{doc_type}: {title}

{content}
"""


# ✅ USE FINAL DATASET (IMPORTANT FIX)
with open("final_dataset.txt", "r", encoding="utf-8") as f:
    text = f.read()


docs = text.split("============================================================")

documents = []

for doc in docs:
    if doc.strip() == "":
        continue

    doc_type = extract_field(r"TYPE:\s*(.*)", doc)
    course_id = extract_field(r"COURSE_ID:\s*(.*)", doc, "N/A")

    page_content = build_page_content(doc)

    documents.append(
        Document(
            page_content=page_content,
            metadata={
                "source": "catalog",
                "type": doc_type,
                "course_id": course_id
            }
        )
    )


print(f"✅ Total documents created: {len(documents)}")