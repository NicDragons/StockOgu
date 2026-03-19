import os
import logging
import requests
import urllib.parse
from dotenv import load_dotenv
from duckduckgo_search import DDGS  # 추가된 패키지

load_dotenv()

# 로깅 설정
logger = logging.getLogger(__name__)

# (기존 fetch_naver_news 함수는 그대로 둡니다)
def fetch_naver_news(query: str = "증시 OR 경제 주요 뉴스", display: int = 15) -> str:
    """네이버 API를 활용해 경제/주식 등 최신 주요 뉴스를 검색합니다."""
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        return "네이버 API 키가 설정되지 않아 뉴스를 검색할 수 없습니다."
        
    url = f"https://openapi.naver.com/v1/search/news.json?query={urllib.parse.quote(query)}&display={display}"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        items = data.get("items", [])
        if not items:
            return f"'{query}'에 대한 뉴스 검색 결과가 없습니다."
            
        news_texts = []
        for item in items:
            title = item.get('title', '').replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
            description = item.get('description', '').replace('<b>', '').replace('</b>', '').replace('&quot;', '"')
            link = item.get('link', '')
            news_texts.append(f"- [{title}] {description} (출처: {link})")
            
        return "\n".join(news_texts)
    except Exception as e:
        logger.error(f"네이버 뉴스 검색 도구 실행 중 오류 발생: {e}")
        return f"뉴스 검색 중 오류가 발생했습니다: {e}. 알려진 지식으로만 답변하세요."

# 새롭게 교체할 웹 검색 함수
def web_search(query: str, max_results: int = 3) -> str:
    """사용자 질문에 대해 실시간 웹 검색(DuckDuckGo)을 수행합니다."""
    logger.info(f"에이전트가 웹 검색을 실행합니다. 검색어: {query}")
    
    try:
        # DuckDuckGo 검색 실행
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return f"'{query}'에 대한 웹 검색 결과가 없습니다."
        
        # 검색 결과를 에이전트가 읽기 편하게 포맷팅
        search_texts = [
            f"- [{res.get('title', '제목 없음')}] {res.get('body', '내용 없음')} (출처: {res.get('href', 'URL 없음')})" 
            for res in results
        ]
        return "\n".join(search_texts)
        
    except Exception as e:
        logger.error(f"웹 검색 도구 실행 중 오류 발생: {e}")
        return f"웹 검색 중 네트워크 오류가 발생했습니다: {e}. 알려진 지식으로만 답변하세요."