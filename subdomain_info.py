import json
import os
import asyncio
from datetime import datetime, timedelta
from pymongo import MongoClient
import threading


def add_subdomains_to_mongo(col, domain):
    subdomain_file = f"{domain.split('.')[0]}-allsub"
    if os.path.exists(subdomain_file):
        with open(subdomain_file, 'r') as f:
            fresh = False if col.count_documents({}) < 1 else "ready"
                
            for subdomain in f:
                subdomain = subdomain.strip()
                existing_subdomain = col.find_one({"sub": subdomain})
                if not existing_subdomain:
                    final = {
                        "sub": subdomain,
                        "status": None,
                        "tech": None,
                        "fresh": fresh,
                        "status_changed": False,
                        "tech_changed": False,
                        "timestamp": datetime.utcnow()
                    }
                    col.insert_one(final)

def extract_fields(line):
    parsed_data = json.loads(line)

    input_value = parsed_data.get("input")
    status_code = parsed_data.get("status_code")
    tech_used = parsed_data.get("tech", None)
    tech_used_str = ', '.join(tech_used) if tech_used else None

    return input_value, status_code, tech_used_str

def update_subdomain_info(col, domain):
    filename = f'{domain.split(".")[0]}-json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            for line in f:
                query, status, tech = extract_fields(line)

                existing_subdomain = col.find_one({"sub": query})
                if existing_subdomain:
                    existing_fresh = existing_subdomain["fresh"]
                    existing_status = existing_subdomain["status"]
                    existing_tech = existing_subdomain["tech"]

                    if existing_fresh == "ready":
                        col.update_one({"sub": query}, {"$set": {"fresh": True}})

                    if status != existing_status:
                        col.update_one({"sub": query}, {"$set": {"status": status, "status_changed": f"{existing_status}:{status}"}})
                    else:
                        col.update_one({"sub": query}, {"$set": {"status": status}})

                    if tech != existing_tech:
                        col.update_one({"sub": query}, {"$set": {"tech": tech, "tech_changed": f"{existing_tech}:{tech}"}})
                    else:
                        col.update_one({"sub": query}, {"$set": {"tech": tech}})

async def update_fresh_after_two_days(col, subdomain_id, field_name):
    await asyncio.sleep(24 * 60 * 60 * 2)  # Sleep for two days
    col.update_one({"_id": subdomain_id}, {"$set": {field_name: False}})

def set_stale_subdomains(col, field_name):
    stale_subdomains = col.find({field_name: {"$ne": False}})
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    update_tasks = [update_fresh_after_two_days(col, subdomain["_id"], field_name) for subdomain in stale_subdomains]

    if update_tasks:
        loop.run_until_complete(asyncio.gather(*update_tasks))

    loop.close()
