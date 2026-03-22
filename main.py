import os
from scraper import get_naver_news, get_weather_info
from summarizer import summarize_news
from messenger import send_telegram_message

def main():
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not gemini_api_key or not telegram_bot_token or not telegram_chat_id:
        print("Missing required environment variables.")
        print("Set GEMINI_API_KEY, TELEGRAM_BOT_TOKEN, and TELEGRAM_CHAT_ID in environment or secrets.")
        import sys
        sys.exit(1)

    print("Scraping news...")
    news_text = get_naver_news()
    weather_text = get_weather_info()
    
    combined_text = news_text + "\n" + weather_text
    
    print("Summarizing with Gemini and sending to Telegram...")
    max_retries = 2
    for attempt in range(max_retries):
        try:
            summary = summarize_news(combined_text, gemini_api_key)
            print("Summary generated.")
            
            print("Sending message to Telegram...")
            send_telegram_message(telegram_bot_token, telegram_chat_id, summary)
            print("Successfully processed and sent.")
            break  # 성공 시 루프 탈출, 재발송 방지
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("Retrying in 5 seconds...")
                import time
                time.sleep(5)
            else:
                print("Max retries reached. Exiting.")
                import sys
                sys.exit(1)

if __name__ == "__main__":
    main()