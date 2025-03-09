import os
import pymongo
import requests
from dotenv import load_dotenv
import json

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
MY_DB = os.getenv('MY_DB')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
TEL_TOKEN = os.getenv('TEL_TOKEN')
TEL_CHANELL_ID = os.getenv('TEL_CHANELL_ID')


def initialize_mongo_collection(domain):
    myclient = pymongo.MongoClient(BASE_URL)
    mydb = myclient[MY_DB]
    mycol = mydb[domain]
    return mycol

def fetch_domains_from_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)  # Replace with your MongoDB connection details
    db = client["mydatabase"]  # Replace with your database name
    domains_collection = db["domains"]  # Replace with your collection name
    
    domains = []
    for doc in domains_collection.find({}, {"domain": 1, "active": 1}):
        domains.append({
            "domain": doc.get("domain"),
            "active": doc.get("active", False)  # Default to False if 'active' field is missing
        })
    
    client.close()
    return domains

def send_data_to_discord(sub):
    webhook_url = WEBHOOK_URL
    
    data = {
        "username": "Subdomain Alert",
        "embeds": [
            {
                "title": "New Subdomain Detected",
                "description": f"A new subdomain has been detected: `{sub}`",
                "color": 65280,  # Green color
            }
        ]
    }
    try:
        response = requests.post(webhook_url, json=data)
    except Exception as e:
        print(f"Error sending new subdomain: {e}")
        return None


def send_data_to_telegram(sub, tech, status):
    bot_token = TEL_TOKEN
    chat_id = TEL_CHANELL_ID

    # انتخاب آیکون بر اساس status code
    if 200 <= status < 300:
        status_icon = "🟢"
    elif 300 <= status < 400:
        status_icon = "🟡"
    else:
        status_icon = "🔴"

    message = (
        f"🚨 New Subdomain Detected:\n"
        f"🔹 Subdomain: {sub}\n"
        f"🔹 Tech: {tech}\n"
        f"🔹 Status: {status_icon} {status}"
    )

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # بررسی موفقیت درخواست
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")
