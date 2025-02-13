import requests

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

# Example usage
send_data_to_discord("newsub.example.com")