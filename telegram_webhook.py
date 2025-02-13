import requests

def send_data_to_telegram(sub):
    bot_token = TEL_TOKEN
    chat_id = TEL_CHANELL_ID
    message = f"🚨 New Subdomain Detected:\n`{sub}`"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    
    try:
        response = requests.post(url, json=data)
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")
