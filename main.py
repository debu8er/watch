import time
from database import (
    initialize_mongo_collection,
    fetch_domains_from_mongodb
)
from fetch_subdomains import fetch_subdomains
from subdomain_info import (
    add_subdomains_to_mongo,
    update_subdomain_info,
)

def process_domain(domain,active):
    print(f"Checking subdomains for {domain}")
    fetch_subdomains(domain,active)
    
    mycol = initialize_mongo_collection(domain)
    add_subdomains_to_mongo(mycol, domain)
    update_subdomain_info(mycol, domain)
    

def main():
    while True:
        domains_to_watch = fetch_domains_from_mongodb()
        for domain in domains_to_watch:
            process_domain(domain["domain"],domain["active"])
        print("Sleeping for 1 min...")
        time.sleep(60)

if __name__ == "__main__":
    main()
