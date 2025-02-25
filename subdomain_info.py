import json
import os
from datetime import datetime, timedelta
from database import send_data_to_discord, send_data_to_telegram
from pymongo import MongoClient, UpdateOne, InsertOne

def add_subdomains_to_mongo(col, domain):
    subdomain_file = f"results/{domain}-allsub"
    if os.path.exists(subdomain_file):
        with open(subdomain_file, 'r') as f:

            if col.count_documents({}) > 0:
                fresh = False
            else:
                fresh = "first"

            bulk_operations = []

            for subdomain in f:
                subdomain = subdomain.strip()
                if not col.find_one({"sub": subdomain}):
                    document = {
                        "sub": subdomain,
                        "status": None,
                        "tech": None,
                        "fresh": fresh,
                        "status_changed": False,
                        "tech_changed": False,
                        "createdAt": datetime.utcnow(),
                        "updatedAt": datetime.utcnow()  # Initialize the updatedAt field
                    }
                    print("The Script Start Add data to database")
                    bulk_operations.append(InsertOne(document))
                    print("The Script Done Add data to database")


            if bulk_operations:
                col.bulk_write(bulk_operations)

def extract_fields(line):
    parsed_data = json.loads(line)
    input_value = parsed_data.get("input")
    status_code = parsed_data.get("status_code")
    tech_used = parsed_data.get("tech", None)
    tech_used_str = ', '.join(tech_used) if tech_used else None
    return input_value, status_code, tech_used_str

def update_subdomain_info(col, domain):
    filename = f'results/{domain}-json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            bulk_operations = []

            for line in f:
                query, status, tech = extract_fields(line)
                existing_subdomain = col.find_one({"sub": query})

                if existing_subdomain:
                    existing_status = existing_subdomain["status"]
                    existing_tech = existing_subdomain["tech"]

                    update_data = {}

                    if tech != existing_tech:
                        update_data["tech"] = tech
                        update_data["tech_changed"] = f"{existing_tech}:{tech}"
                    if status != existing_status:
                        update_data["status"] = status
                        update_data["status_changed"] = f"{existing_status}:{status}"

                    if update_data:
                        update_data["updatedAt"] = datetime.utcnow()
                        if existing_subdomain["fresh"] == False:
                            existing_subdomain["fresh"] = "live"
                            update_data["fresh"] = "live"
                            send_data_to_telegram(query, tech, status)

                        bulk_operations.append(
                            UpdateOne({"sub": query}, {"$set": update_data})
                        )

            if bulk_operations:
                col.bulk_write(bulk_operations)

def set_stale_subdomains(col, field_name):
    two_days_ago = datetime.utcnow() - timedelta(days=2)
    col.update_many(
        {field_name: {"$ne": False}, "updatedAt": {"$lt": two_days_ago}},
        {"$set": {field_name: False}}
    )
