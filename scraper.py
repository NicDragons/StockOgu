import requests
from bs4 import BeautifulSoup

def get_naver_news():
    categories = {
        '정치': '100',
        '경제': '101',
        '사회': '102',
        '생활문화': '103',
        '국제': '104',
        'IT과학': '105'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    news_data = []
    
    for category_name, sid in categories.items():
        url = f"https://news.naver.com/section/{sid}"
        try:
            res = requests.get(url, headers=headers)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Naver news headlines are usually in sa_text_strong
            headlines = soup.find_all('strong', class_='sa_text_strong')
            
            category_news = []
            for h in headlines:
                title = h.text.strip()
                if title and title not in category_news:
                    category_news.append(title)
                if len(category_news) >= 8: # Collect slightly more to give Gemini options
                    break
                    
            if category_news:
                news_data.append(f"[{category_name}]")
                for news in category_news:
                    news_data.append(f"- {news}")
                news_data.append("")
        except Exception as e:
            print(f"Error scraping {category_name}: {e}")
            
    return "\n".join(news_data)

def get_weather_info():
    # Attempting to get weather from Naver search
    url = "https://search.naver.com/search.naver?query=오늘날씨"
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        weather_text = soup.select_one('.temperature_text').text.strip() if soup.select_one('.temperature_text') else ""
        summary = soup.select_one('.summary').text.strip() if soup.select_one('.summary') else ""
        
        if weather_text and summary:
            return f"[날씨]\n- {weather_text}, {summary}\n"
    except Exception as e:
        print(f"Error scraping weather: {e}")
    
    return "[날씨]\n- 오늘 날씨 정보를 가져올 수 없습니다.\n"

if __name__ == "__main__":
    print(get_naver_news())
    print(get_weather_info())
