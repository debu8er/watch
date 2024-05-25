import os
import requests
import re
from database import initialize_mongo_collection

def fetch_subdomains(domain):
    # Fetch subdomains from different sources
    crtsh_subdomains = fetch_crtsh_subdomains(domain)
    abuseipdb_subdomains = fetch_abuseipdb_subdomains(domain)
    subfinder = fetch_subfinder_subdomains(domain)
    # dnsbrute = fetch_dnsbrute_subdomains(domain)
    
    # Combine subdomains from different sources
    all_subdomains = crtsh_subdomains + abuseipdb_subdomains
    
    # Save all subdomains to a file
    save_subdomains_to_file(domain, all_subdomains)

def fetch_crtsh_subdomains(domain):
    try:
        crtsh_url = f'https://crt.sh/?q={domain}&output=json'
        crtsh_response = requests.get(crtsh_url)

        crtsh_response.raise_for_status()  # Raise an exception for HTTP errors

        crtsh_data = crtsh_response.json()
        common_names = {entry["name_value"] for entry in crtsh_data}
        return list(common_names)
    except requests.RequestException as e:
        print(f"An error occurred during CRTSH request: {e}")
        return []

def fetch_abuseipdb_subdomains(domain):
    try:
        abuseipdb_url = f'https://www.abuseipdb.com/whois/{domain}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        cookies = {'abuseipdb_session': 'YOUR-session'}
        abuseipdb_response = requests.get(abuseipdb_url, headers=headers, cookies=cookies)

        abuseipdb_response.raise_for_status()  # Raise an exception for HTTP errors

        abuseipdb_data = abuseipdb_response.text
        regex_pattern = r'<li>(\w.*)<\/li>'
        subdomains = re.findall(regex_pattern, abuseipdb_data)
        return [subdomain + f'.{domain}' for subdomain in subdomains]
    except requests.RequestException as e:
        print(f"An error occurred during AbuseIPDB request: {e}")
        return []

def fetch_subfinder_subdomains(domain):
    try:
        os.system(f'subfinder -all -d {domain} -silent > {domain}-subfinder')

    except IOError as e:
        print(f"An error occurred during file merging/sorting: {e}")


def run_alterx_dnsx(domain):
    try:
        collection = initialize_mongo_collection(domain)

        alterx_sub = (f'{domain}-alterx-allsub')
        result = list(collection.find({}))

        if len(result) != 0:
            with open(alterx_sub,'w') as f:
                for i in collection.find({}):
                    f.writelines(('%s\n' % i["sub"]))
            command = f"cat {alterx_sub} | alterx -silent | dnsx -silent > {domain}-dnsbrute"
            os.system(command)
        
        else:
            return False
    except IOError as e:
        print(f"An error occurred during file merging/sorting: {e}")


def merge_and_sort_files(domain, subfinder, crtabuse, dnsbrute, allsub):
    try:
        with open(subfinder, 'r') as file1, open(crtabuse, 'r') as file2, open(allsub, 'w') as output:
            
            lines = set(file1.readlines() + file2.readlines())
            
            if run_alterx_dnsx(domain):
                with open(dnsbrute, 'r') as file3:
                    lines.update(file3.readlines())
            
            output.writelines(sorted(lines))
    
    except IOError as e:
        print(f"An error occurred during file merging/sorting: {e}")


def save_subdomains_to_file(domain, subdomains):
    try:
        subdomains_file = f'{domain}-crtabuse'

        with open(subdomains_file, 'w') as file:
            file.writelines([subdomain + '\n' for subdomain in subdomains])

        subfinder = f'{domain}-subfinder'
        crtabuse = f'{domain}-crtabuse'
        dnsbrute = f'{domain}-dnsbrute'
        allsub = f'{domain}-allsub'

        merge_and_sort_files(domain, subfinder, crtabuse, dnsbrute, allsub)
        os.system(f'httpx -l {domain}-allsub -sc -td -silent -json > {domain}-json')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_subdomains(domain)
