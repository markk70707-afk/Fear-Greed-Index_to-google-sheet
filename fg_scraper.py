import json
import sys
import cloudscraper

url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"

# Desktop Chrome 환경 핑거프린팅
scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://www.cnn.com/markets"
}

try:
    res = scraper.get(url, headers=headers, timeout=15)
    
    if res.status_code == 200:
        data = res.json()
        if 'fear_and_greed' in data:
            score = round(data['fear_and_greed']['score'])
            rating = data['fear_and_greed']['rating']

            result = {"score": score, "rating": rating}

            with open('fg_data.json', 'w') as f:
                json.dump(result, f)

            print(f"Success: {score} ({rating})")
            sys.exit(0)

    # 차단 시 터지지 않고 기존 JSON 데이터 유지
    print(f"CNN API 호출 실패 (HTTP Status: {res.status_code}). 기존 데이터를 유지합니다.")
    sys.exit(0)

except Exception as e:
    print(f"스크래핑 예외 발생: {e}. 기존 데이터를 유지합니다.")
    sys.exit(0)
