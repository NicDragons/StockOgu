import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def bad_tool(query: str) -> str:
    pass

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(tools=[bad_tool])
)
try:
    resp = chat.send_message("Use bad tool with 'test' query")
    print(resp.text)
except Exception as e:
    print("Error:", type(e).__name__)
    print(e)
