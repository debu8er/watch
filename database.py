import pymongo

def initialize_mongo_collection(domain):
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb[domain.split(".")[0]]
    return mycol

def fetch_domains_from_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection details
    db = client["mydatabase"]  # Replace with your database name
    domains_collection = db["domains"]  # Replace with your collection name
    domain_names = domains_collection.distinct("domain")
    client.close()
    return domain_names