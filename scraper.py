import requests
from bs4 import BeautifulSoup

def get_google_news():
    # GitHub 서버(해외 IP)에서 네이버 뉴스 접속 시 봇 차단(캡챠)이 발생하여 빈 텍스트를 반환하는 문제를 해결하기 위해,
    # 차단이 전혀 없는 Google News RSS 피드를 사용합니다.
    categories = {
        '정치/사회': 'NATION',
        '경제/증권': 'BUSINESS',
        '국제': 'WORLD',
        'IT/과학': 'TECHNOLOGY',
        '생활/문화': 'ENTERTAINMENT'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    news_data = []
    
    for category_name, topic in categories.items():
        url = f"https://news.google.com/rss/headlines/section/topic/{topic}?hl=ko&gl=KR&ceid=KR:ko"
        try:
            res = requests.get(url, headers=headers)
            res.raise_for_status()
            
            # html.parser를 이용하여 XML 형태의 RSS 파싱
            soup = BeautifulSoup(res.content, 'html.parser')
            
            items = soup.find_all('item')
            category_news = []
            
            for item in items:
                title = item.title.text.strip()
                if title and title not in category_news:
                    category_news.append(title)
                if len(category_news) >= 8: # Gemini에게 줄 넉넉한 기사 수
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
    url = "https://search.naver.com/search.naver?query=전국오늘날씨"
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        weather_text = soup.select_one('.temperature_text').text.strip() if soup.select_one('.temperature_text') else ""
        summary = soup.select_one('.summary').text.strip() if soup.select_one('.summary') else ""
        
        if weather_text and summary:
            return f"[날씨]\n- {weather_text}, {summary}\n"
    except Exception as e:
        print(f"Error scraping weather: {e}")
    
    return "[날씨]\n- 오늘 날씨 정보를 가져올 수 없습니다.\n"

def get_naver_news():
    # 하위 호환성을 위해 유지 (main.py 변경 최소화)
    return get_google_news()

if __name__ == "__main__":
    print(get_google_news())
