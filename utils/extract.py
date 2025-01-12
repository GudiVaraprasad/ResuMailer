import textract
from gensim.summarization import summarize
import tempfile
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time

def save_temp_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as temp_file:
        temp_file.write(uploaded_file.read())
        return temp_file.name

def extract_text_from_file(file_path):
    raw_text = textract.process(file_path)
    clean_text = raw_text.decode('utf-8', errors='ignore').replace('\n', ' ').replace('\x0c', '').strip()
    os.remove(file_path)
    return clean_text

def extract_text_from_url(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    sections = ["Responsibilities", "Duties", "Qualifications", "Requirements", "Skills", "Overview", "Minimum Qualifications", "Preferred Qualifications"]
    extracted_text = []

    for section in sections:
        pattern = re.compile(section, re.IGNORECASE)
        header = soup.find(lambda tag: tag.name in ["h2", "h3", "strong", "b", "p"] and pattern.search(tag.get_text(strip=True)))

        if header:
            next_element = header.find_next_sibling()
            while next_element and next_element.name not in ["h2", "h3", "strong", "b"]:
                if next_element.name in ["ul", "ol"]:
                    extracted_text.extend([li.get_text(strip=True) for li in next_element.find_all("li")])
                elif next_element.name in ["div", "p"]:
                    extracted_text.append(next_element.get_text(separator=" ").strip())
                next_element = next_element.find_next_sibling()

    if not extracted_text:
        largest_text_block = max(
            (tag.get_text(strip=True) for tag in soup.find_all(["div", "p"]) if len(tag.get_text(strip=True)) > 100),
            key=len,
            default=""
        )
        extracted_text.append(largest_text_block)

    return " ".join([text for text in extracted_text if text]).strip() or "No relevant job details found."

def summarize_text(text, word_count=600):
    return summarize(text, word_count=word_count) if len(text.split()) > 50 else text

def extract_resume(uploaded_file):
    if not uploaded_file:
        return "No file uploaded."
    temp_file_path = save_temp_file(uploaded_file)
    resume_text = extract_text_from_file(temp_file_path)
    return summarize_text(resume_text)

def extract_jobdesc(url):
    job_text = extract_text_from_url(url)
    return summarize_text(job_text)