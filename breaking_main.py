import os
import sys
import time

def main():
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not gemini_api_key or not telegram_bot_token or not telegram_chat_id:
        print("Missing required environment variables.")
        sys.exit(1)

    # 1. Load history (create if not exists)
    history_file = "history_breaking.txt"
    history_list = []
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            history_list = [line.strip() for line in f if line.strip()]
    else:
        # Create empty file to avoid git add error
        with open(history_file, "w", encoding="utf-8") as f:
            pass

    # 2. Scrape breaking news with history
    from scraper import get_breaking_news
    print("Scraping breaking news...")
    breaking_text, new_titles = get_breaking_news(history_list)
    
    # 3. If there are new breaking news
    if breaking_text and new_titles:
        print(f"Found {len(new_titles)} new breaking news items.")
        from summarizer import summarize_breaking_news
        from messenger import send_telegram_message
        
        max_retries = 2
        for attempt in range(max_retries):
            try:
                print("Summarizing with Gemini and sending to Telegram...")
                breaking_summary = summarize_breaking_news(breaking_text, gemini_api_key)
                print("Breaking news summary generated.")
                
                send_telegram_message(telegram_bot_token, telegram_chat_id, breaking_summary)
                print("Successfully processed and sent breaking news.")
                
                # 4. Save history
                with open(history_file, "a", encoding="utf-8") as f:
                    for title in new_titles:
                        f.write(title + "\n")
                print("History updated.")
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for breaking news: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    print("Max retries reached for breaking news. Exiting.")
                    sys.exit(1)
    else:
        print("No new breaking news found.")

if __name__ == "__main__":
    main()
