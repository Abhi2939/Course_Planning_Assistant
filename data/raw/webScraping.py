import requests
from bs4 import BeautifulSoup
import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_title(title):
    title = re.sub(r'credit:.*', '', title)
    return title.strip()

def extract_prereq(text):
    if "Prerequisite:" in text:
        prereq = text.split("Prerequisite:")[-1]
        prereq = prereq.split(".")[0]
        prereq = re.sub(r'This course satisfies.*', '', prereq)
        return prereq.strip()
    return "None"

def remove_prereq_from_desc(text):
    if "Prerequisite:" in text:
        return text.split("Prerequisite:")[0].strip()
    return text

def clean_description(text):
    text = re.sub(r'Credit is not given.*?\.', '', text)
    text = re.sub(r'This course satisfies.*', '', text)
    return text.strip()

def extract_course_id(title):
    parts = title.split()
    return parts[0] + " " + parts[1]

url = "https://catalog.illinois.edu/courses-of-instruction/cs/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

courses = soup.find_all("div", class_="courseblock")

with open("courses.txt", "w", encoding="utf-8") as f:
    for course in courses[:25]:

        title_tag = course.find("p", class_="courseblocktitle")
        desc_tag = course.find("p", class_="courseblockdesc")

        if not title_tag or not desc_tag:
            continue

        title_raw = clean_text(title_tag.get_text())
        title = clean_title(title_raw)

        desc_raw = clean_text(desc_tag.get_text())

        prereq = extract_prereq(desc_raw)
        desc = remove_prereq_from_desc(desc_raw)
        desc = clean_description(desc)

        course_id = extract_course_id(title)

        source = f"{url} | {course_id}"

        f.write(f"COURSE_ID: {course_id}\n")
        f.write(f"TITLE: {title}\n\n")
        f.write(f"DESCRIPTION:\n{desc}\n\n")
        f.write(f"PREREQUISITES:\n{prereq}\n\n")
        f.write(f"SOURCE:\n{source}\n")
        f.write("=" * 50 + "\n\n")