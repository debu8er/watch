import requests 
 
def send_data_to_telegram(sub): 
    bot_token = "7367570054:AAE9r_Q9sXyuAhNeW5Nqp3cWajBwIZd1So8" 
    chat_id = "-1002428661648" 
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
 
# Example usage 
send_data_to_telegram("newsub.example.com")
