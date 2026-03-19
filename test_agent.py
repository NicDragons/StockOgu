import os
from dotenv import load_dotenv

load_dotenv()

from tools import fetch_naver_news, web_search
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_instruction = "test"

try:
    agent_chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[fetch_naver_news, web_search]
        )
    )
    print("Chat session created.")
    
    response = agent_chat.send_message("오늘 아침 브리핑 양식대로 출력해 줘")
    print("Response received:")
    print(response.text)
except Exception as e:
    import traceback
    traceback.print_exc()
