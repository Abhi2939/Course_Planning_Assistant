import requests
from bs4 import BeautifulSoup
import re
import uuid
import os
from datetime import datetime


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def clean_title(title):
    title = re.sub(r'credit:.*', '', title, flags=re.IGNORECASE)
    return title.strip()


def extract_prereq(text):
    """
    Improved extraction:
    Handles:
    - Prerequisite:
    - Prerequisites:
    - Prereq:
    """
    match = re.search(r'Prereq.*?:\s*(.*?)(?:\.|$)', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "None"


def clean_prereq(prereq):
    # Fix broken words
    fixes = {
        "MA TH": "MATH",
        "E CE": "ECE",
        "ST AT": "STAT",
        "BI OE": "BIOE",
        "AS RM": "ASRM"
    }
    for k, v in fixes.items():
        prereq = prereq.replace(k, v)

    # Normalize course codes
    prereq = re.sub(r'([A-Z]{2,4}\s?\d{3})', r' \1 ', prereq)
    prereq = re.sub(r'\s+', ' ', prereq)

    # Clean commas
    prereq = re.sub(r'\s+,', ',', prereq)
    prereq = re.sub(r',\s+', ', ', prereq)

    # Preserve logical meaning
    prereq = prereq.replace(";", "\nAND\n")
    prereq = re.sub(r'\bor\b', 'OR', prereq, flags=re.IGNORECASE)

    return prereq.strip()


def remove_prereq_from_desc(text):
    return re.split(r'Prereq.*?:', text, flags=re.IGNORECASE)[0].strip()


def clean_description(text):
    text = re.sub(r'Credit is not given.*?\.', '', text)
    text = re.sub(r'This course satisfies.*', '', text)
    text = re.sub(r'Prereq.*?:.*', '', text)
    return text.strip()


def extract_course_id(title):
    parts = title.split()
    return parts[0] + " " + parts[1]


url = "https://catalog.illinois.edu/courses-of-instruction/cs/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print("❌ Failed to fetch page")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

courses = soup.find_all("div", class_="courseblock")

print("📊 Total courses found:", len(courses))

output_path = os.path.join(os.path.dirname(__file__), "courses.txt")

date_accessed = datetime.now().strftime("%Y-%m-%d")

with open(output_path, "w", encoding="utf-8") as f:
    for course in courses:   # ✅ removed limit

        title_tag = course.find("p", class_="courseblocktitle")
        desc_tag = course.find("p", class_="courseblockdesc")

        if not title_tag or not desc_tag:
            continue

        try:
            # -------- TITLE -------- #
            title_raw = clean_text(title_tag.get_text())
            title = clean_title(title_raw)

            # -------- DESCRIPTION -------- #
            desc_raw = clean_text(desc_tag.get_text())

            prereq_raw = extract_prereq(desc_raw)
            prereq_clean = clean_prereq(prereq_raw)

            desc = remove_prereq_from_desc(desc_raw)
            desc = clean_description(desc)

            # -------- COURSE ID -------- #
            course_id = extract_course_id(title)

            # -------- CHUNK ID -------- #
            chunk_id = f"{course_id.replace(' ', '')}_{str(uuid.uuid4())[:6]}"

            # -------- WRITE -------- #
            f.write(f"TYPE: COURSE\n")
            f.write(f"COURSE_ID: {course_id}\n")
            f.write(f"TITLE: {title}\n\n")

            f.write(f"DESCRIPTION:\n{desc}\n\n")

            f.write(f"PREREQUISITES:\n{prereq_clean}\n\n")

            f.write(f"SOURCE:\n{url}\n")
            f.write(f"DATE_ACCESSED: {date_accessed}\n")
            f.write(f"CHUNK_ID: {chunk_id}\n")

            f.write("=" * 60 + "\n\n")

            print(f"✅ Processed: {course_id}")

        except Exception as e:
            print(f"⚠️ Skipped a course due to error: {e}")

print("\n🎉 courses.txt generated successfully!")
print("📁 Saved at:", output_path)