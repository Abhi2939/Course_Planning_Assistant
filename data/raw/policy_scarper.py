import requests
from bs4 import BeautifulSoup
import re
import uuid
import os
from datetime import datetime


# ---------- CLEAN TEXT ----------
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# ---------- CHUNK TEXT ----------
def chunk_text(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunk_size - overlap

    return chunks


# ---------- SCRAPE PAGE ----------
def scrape_page(url, doc_type="PROGRAM", title_override=None):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return []

    if response.status_code != 200:
        print(f"❌ Failed ({response.status_code}): {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # ✅ Extract MAIN content
    main_content = soup.find("div", {"id": "main-content"}) or soup.find("main")

    if main_content:
        content = main_content.get_text(separator=" ")
    else:
        content = soup.get_text(separator=" ")

    content = clean_text(content)

    # Remove junk
    content = re.sub(r'Skip to main content', '', content)
    content = re.sub(r'Back to top', '', content)

    # Chunking
    chunks = chunk_text(content)

    # Title
    title = title_override if title_override else (
        soup.title.string.strip() if soup.title else "Unknown Title"
    )

    date_accessed = datetime.now().strftime("%Y-%m-%d")

    documents = []

    for chunk in chunks:
        if len(chunk) < 50:
            continue

        chunk_id = f"{doc_type}_{str(uuid.uuid4())[:8]}"

        doc = f"""TYPE: {doc_type}
TITLE: {title}

CONTENT:
{chunk}

SOURCE:
{url}
DATE_ACCESSED: {date_accessed}
CHUNK_ID: {chunk_id}
{"="*60}

"""
        documents.append(doc)

    print(f"✅ Extracted {len(documents)} chunks from {doc_type}")

    return documents


# ---------- URLS ----------
urls = [
    # PROGRAM PAGES
    ("https://catalog.illinois.edu/undergraduate/engineering/computer-science-bs/", "PROGRAM", "CS Major Requirements"),
    ("https://cs.illinois.edu/academics/undergraduate/degree-program-options/bs-computer-science", "PROGRAM", "CS Degree Structure"),

    # POLICY PAGE (WORKING URL)
    ("https://studentcode.illinois.edu/article3/part1/3-101/", "POLICY", "Academic Policies"),
]


# ---------- OUTPUT ----------
output_path = os.path.join(os.path.dirname(__file__), "extra_docs.txt")

with open(output_path, "w", encoding="utf-8") as f:
    for url, doc_type, title in urls:
        print(f"\n🔍 Scraping: {url}")

        docs = scrape_page(url, doc_type, title)

        for d in docs:
            f.write(d)

print("\n🎉 extra_docs.txt generated successfully!")
print("📁 Saved at:", output_path)