from google import genai

def summarize_news(news_text, api_key):
    # 최신 google-genai 패키지 문법 적용
    client = genai.Client(api_key=api_key)
    
    from datetime import datetime
    import pytz
    
    kst = pytz.timezone('Asia/Seoul')
    today_str = datetime.now(kst).strftime("%Y년 %m월 %d일 %A")

    prompt = f"""
다음은 방금 스크래핑한 각 분야별 주요 뉴스 헤드라인과 날씨 정보입니다.
이를 바탕으로 아래 양식에 맞추어 오늘 주요 뉴스 브리핑을 작성해주세요. 
사용자가 읽기 편하고 자연스러운 문장 ('~습니다/니다')으로 작성해야 합니다.

[중요 요청사항 - 주식 분석 추가]
각 분야별(경제, 증권금융, IT과학, 국제 등) 뉴스를 요약한 뒤, 해당 이슈로 인해 수혜를 보거나 주목받을 수 있는 관련 주식을 5개씩(국내/해외 혼합) 분석하여 추천해주세요.
주식 추천 시 다음 형식을 반드시 지켜주세요:
1. [국내] / [해외] 여부를 명칭 앞에 명확히 표시
2. 국내 주식의 경우 [코스피] 인지 [코스닥] 인지 상세 시장 분류 추가
3. 해당 주식이 어떤 '테마주'(예: AI반도체, 2차전지, 웹툰, 로봇 등)에 속하는지 구체적인 이유나 테마 명시

양식 예시: 
[{today_str}] 주요 뉴스 브리핑

<경 제>
• [경제 주요 뉴스 브리핑]
• [경제 주요 뉴스 브리핑]

💡 [관련 주식 5선 요약]
1. [해외] 엔비디아 (테마: AI 반도체 대장주)
2. [국내/코스피] SK하이닉스 (테마: HBM 고대역폭 메모리)
3. [국내/코스닥] 한미반도체 (테마: 반도체 후공정 장비)
4. [해외] 마이크로소프트 (테마: 생성형 AI 플랫폼)
5. [국내/코스피] 네이버 (테마: 국내 독자 LLM AI)

<IT과학>
• [IT과학 뉴스 브리핑]
💡 [관련 주식 5선 요약]
...

(다른 섹터도 위 양식과 동일한 방식으로 작성. 단, 사회/날씨 등 주식과 직접 연관이 떨어지는 분야는 주식 추천을 생략해도 됩니다.)

---
스크래핑된 뉴스 데이터:
{news_text}
"""
    
    # Pro 모델은 무료 속도 제한(Rate Limit)이 매우 엄격하므로, 할당량이 큰 최신 Flash 모델 사용
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"gemini-2.5-flash 모델 에러, 대체 모델로 재시도 중... Error: {e}")
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt
        )
        return response.text
