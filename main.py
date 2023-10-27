import threading
import time
import pymongo

from database import (
    initialize_mongo_collection,
    fetch_domains_from_mongodb
)
from fetch_subdomains import fetch_subdomains
from subdomain_info import (
    add_subdomains_to_mongo,
    update_subdomain_info,
    set_stale_subdomains,
)

# Function to fetch domain names from the MongoDB 'domains' collection


def watch_for_domain(domain, interval, stop_flag):
    while not stop_flag.is_set():
        print(f"Checking subdomains for {domain}")
        fetch_subdomains(domain)

        mycol = initialize_mongo_collection(domain)
        add_subdomains_to_mongo(mycol, domain)
        update_subdomain_info(mycol, domain)

        # Create background threads for set_stale_subdomains
        fresh_thread = threading.Thread(target=set_stale_subdomains, args=(mycol, "fresh"))
        status_changed_thread = threading.Thread(target=set_stale_subdomains, args=(mycol, "status_changed"))
        tech_changed_thread = threading.Thread(target=set_stale_subdomains, args=(mycol, "tech_changed"))

        # Set the threads as daemon threads
        fresh_thread.daemon = True
        status_changed_thread.daemon = True
        tech_changed_thread.daemon = True

        # Start all background threads
        fresh_thread.start()
        status_changed_thread.start()
        tech_changed_thread.start()

        print(f"Sleeping for {interval} seconds.")
        time.sleep(interval)

def main():
    # Create a dictionary to store monitored domains and their corresponding threads
    monitored_domains = {}

    while True:
        # Fetch domain names from the 'domains' collection
        domains_to_watch = fetch_domains_from_mongodb()

        # Determine threads to remove
        threads_to_remove = []
        for domain, (thread, stop_flag) in monitored_domains.items():
            if domain not in domains_to_watch:
                stop_flag.set()  # Set the stop flag to signal the thread to stop
                threads_to_remove.append(domain)

        # Stop and remove threads for removed domains
        for domain in threads_to_remove:
            thread, _ = monitored_domains.pop(domain)
            thread.join()  # Wait for the thread to finish
            print(f"Stopped monitoring for removed domain: {domain}")

        # Determine domains to add threads for
        domains_to_add = set(domains_to_watch) - set(monitored_domains.keys())

        # Start threads for new domains
        for domain in domains_to_add:
            stop_flag = threading.Event()
            thread = threading.Thread(target=watch_for_domain, args=(domain, 20, stop_flag))
            thread.daemon = True
            thread.start()
            monitored_domains[domain] = (thread, stop_flag)  # Add the domain, thread, and stop flag to the dictionary

        time.sleep(5)  # Sleep for 5 seconds before checking for changes again

if __name__ == "__main__":
    main()
