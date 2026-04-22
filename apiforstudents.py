import pandas as pd
import requests

from datetime import date,datetime

EVENT_DATETIME = datetime(2026, 4, 25, 11, 0) # 11:00 AM CST on April 25, 2026
if datetime.now() >= EVENT_DATETIME:
    print("Student ingestion is disabled after the event starts.")
    exit()


EXCEL_PATH = "/Users/xavier/Desktop/UWMSRPC/2026rpc.xlsx"
API_URL = "http://127.0.0.1:8000/api/home/students/create/"
USE_PROD = True

TOKEN = "tooekn" # Replace with your actual token for production

import os
import pandas as pd
import requests
from datetime import date

INSERTED_LOG = "/Users/xavier/Desktop/UWMSRPC/inserted_poster_ids.txt"

df = pd.read_excel(EXCEL_PATH).fillna("")


def smart_title(text):
    if not isinstance(text, str):
        return text
    words = text.split()
    result = []
    for w in words:
        if w.isupper():
            result.append(w)
        else:
            result.append(w.capitalize())
    return " ".join(result)


def title_case(text):
    return text.title() if isinstance(text, str) else text


def lower_case(text):
    return text.lower() if isinstance(text, str) else text


def normalize_poster_id(value):
    if pd.isna(value) or value == "":
        return ""
    try:
        return str(int(float(value))).strip()
    except (ValueError, TypeError):
        return str(value).strip()


for col in [
    "First Name",
    "Last Name",
    "Phonetic spelling",
    "Research adviser first name",
    "Research adviser last name",
]:
    if col in df.columns:
        df[col] = df[col].apply(title_case)

if "Title" in df.columns:
    df["Title"] = df["Title"].apply(smart_title)

if "email" in df.columns:
    df["email"] = df["email"].apply(lower_case)

if "Research adviser email" in df.columns:
    df["Research adviser email"] = df["Research adviser email"].apply(lower_case)


headers = {"Content-Type": "application/json"}
if USE_PROD:
    API_URL = "https://api.uwmsrpc26.com/api/home/students/create/"
    headers["Authorization"] = f"Bearer {TOKEN}"


inserted_poster_ids = set()
if os.path.exists(INSERTED_LOG):
    with open(INSERTED_LOG, "r", encoding="utf-8") as f:
        inserted_poster_ids = {line.strip() for line in f if line.strip()}

print(f"Loaded {len(inserted_poster_ids)} poster IDs from {INSERTED_LOG}")


for index, row in df.iterrows():
    first_name = str(row.get("First Name", "")).strip()
    last_name = str(row.get("Last Name", "")).strip()
    email = str(row.get("email", "")).strip().lower()
    full_name = f"{first_name} {last_name}".strip()
    poster_id = normalize_poster_id(row.get("Poster ID", ""))

    if not poster_id:
        print(f"SKIPPED Row {index + 1}: {full_name} has no Poster ID")
        continue

    if poster_id in inserted_poster_ids:
        print(f"SKIPPED Row {index + 1}: {full_name} already inserted with Poster ID {poster_id}")
        continue

    payload = {
        "date": str(date.today()),
        "department": str(row.get("Department", "")).strip(),
        "academic_status": str(row.get("Category", "")).strip(),
        "first_name": first_name,
        "last_name": last_name,
        "phonetic_spelling": str(row.get("Phonetic spelling", "")).strip(),
        "research_adviser_first_name": str(row.get("Research adviser first name", "")).strip(),
        "research_adviser_last_name": str(row.get("Research adviser last name", "")).strip(),
        "research_adviser_email": str(row.get("Research adviser email", "")).strip().lower(),
        "poster_title": str(row.get("Title", "")).strip(),
        "jacket_size": str(row.get("Jacket size", "")).strip(),
        "jacket_gender": str(row.get("Jacket gender", "")).strip(),
        "poster_ID": int(poster_id) if poster_id.isdigit() else poster_id,
        "Name": full_name,
        "email": email,
        "scored_By_Judges": None,
        "finalist": False,
    }

    response = requests.post(API_URL, json=payload, headers=headers)

    if response.status_code == 201:
        print(f"INSERTED Row {index + 1}: {full_name} with Poster ID {poster_id}")
        inserted_poster_ids.add(poster_id)
        with open(INSERTED_LOG, "a", encoding="utf-8") as f:
            f.write(poster_id + "\n")
    else:
        print(f"ERROR Row {index + 1}: {full_name} => {response.status_code}")
        print("     Error:", response.text)