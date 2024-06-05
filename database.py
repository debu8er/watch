import os
import pymongo
import requests
from dotenv import load_dotenv
import json

load_dotenv()

BASE_URL = os.getenv('BASE_URL')
MY_DB = os.getenv('MY_DB')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')


def initialize_mongo_collection(domain):
    myclient = pymongo.MongoClient(BASE_URL)
    mydb = myclient[MY_DB]
    mycol = mydb[domain]
    return mycol

def fetch_domains_from_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection details
    db = client["mydatabase"]  # Replace with your database name
    domains_collection = db["domains"]  # Replace with your collection name
    domain_names = domains_collection.distinct("domain")
    client.close()
    return domain_names

def send_data_to_discord(sub):
    webhook_url = WEBHOOK_URL
    data = {
        "username": "Webhook Name",
        "content": f"{sub}"
    }

    response = requests.post(webhook_url, json=data)
