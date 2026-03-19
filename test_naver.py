import os
import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

print(f"로드된 ID: {client_id}")
print(f"로드된 시크릿: {client_secret}")

url = "https://openapi.naver.com/v1/search/news.json?query=테스트"
headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}

response = requests.get(url, headers=headers)
print(f"\n네이버 응답 코드: {response.status_code}")
print(f"네이버 응답 내용: {response.text}")