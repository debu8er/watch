import os

def fetch_subdomains(domain):
    os.system(f'curl -s "https://crt.sh/?q={domain}&output=json" | jq -r ".[].common_name" | sort -u > {domain.split(".")[0]}-crtsh')
    os.system(f'subfinder -all -d {domain} -silent > {domain.split(".")[0]}-subfinder')
    os.system(f'curl -s "https://www.abuseipdb.com/whois/{domain}" -H "user-agent: firefox" -b "abuseipdb_session=YOUR-session" | grep -E "<li>\w.*</li>" | sed -E "s/<\/?li>//g" | sed -e "s/$/.{domain}/" > {domain.split(".")[0]}-abuse')
    os.system(f'cat {domain.split(".")[0]}-crtsh {domain.split(".")[0]}-subfinder {domain.split(".")[0]}-subfinder | sort -u > {domain.split(".")[0]}-allsub')
    os.system(f'httpx -l {domain.split(".")[0]}-allsub -sc -td -silent -json > {domain.split(".")[0]}-json')