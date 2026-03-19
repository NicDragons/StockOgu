import requests

def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    
    res = requests.post(url, json=payload)
    if res.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {res.text}")
