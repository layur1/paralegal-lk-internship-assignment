import pdfplumber
import re
import os
import json


def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text


def extract_bench(text):
    pattern = r'Before\s*[:\-]?\s*(.+)'
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        line = match.group(1)
        names = re.split(r',|\n', line)
        return [name.strip() for name in names if name.strip()]

    return []


def extract_author(text):
    if not text:
        return []

    patterns = [
        r'Author(?:s)?\s*[:\-]\s*(.+)',
        r'Authored by\s*[:\-]\s*(.+)',
        r'By\s*[:\-]?\s*(.+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            author_line = match.group(1).strip()
            author_line = author_line.splitlines()[0].strip()
            authors = [
                a.strip()
                for a in re.split(r',|;|\band\b', author_line, flags=re.IGNORECASE)
                if a.strip()
            ]
            return authors if authors else [author_line]

    return []


def process_all():
    input_dir = "data"
    output_dir = "output"

    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            path = os.path.join(input_dir, file)
            text = extract_text(path)

            bench = extract_bench(text)
            author = extract_author(text)

            result = {
                "source_file": file,
                "bench": bench,
                "author_judge": author
            }

            out_path = os.path.join(output_dir, file.replace(".pdf", ".json"))

            with open(out_path, "w") as f:
                json.dump(result, f, indent=4)


if __name__ == "__main__":
    process_all()