import requests
import os
from dotenv import load_dotenv
# Airtable Configuration (Replace with your details)
load_dotenv()
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API")
BASE_ID = os.getenv("AIRTABLE_API")
TABLE_NAME = "Sales_Data"

def upload_to_airtable(data):
    """Uploads sales data to Airtable"""
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

    records = [{"fields": row} for row in data]
    response = requests.post(url, json={"records": records}, headers=headers)

    if response.status_code == 200:
        print("✅ Data uploaded successfully to Airtable!")
    else:
        print(f"❌ Error: {response.text}")

    return response.json()
