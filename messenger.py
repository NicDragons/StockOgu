import requests
import time

def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # 텔레그램은 한 번에 전송 가능한 글자 수가 최대 4096자입니다. 
    # 주식 분석 내용이 길어져서 이를 초과하면 전송이 차단되므로 4000자씩 나눠서 보냅니다.
    max_length = 4000
    chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    
    for i, chunk in enumerate(chunks):
        payload = {
            "chat_id": chat_id,
            "text": chunk
        }
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            print(f"Message chunk {i+1} sent successfully")
        else:
            print(f"Failed to send message chunk {i+1}: {res.text}")
        
        # 여러 개로 나뉘어 전송될 때 순서가 꼬이지 않도록 1초 대기
        time.sleep(1)
