import json
import cloudscraper
from datetime import datetime
import pytz

# 오늘 날짜 기반 CDN URL 생성 (차단 회피 목적)
seoul_tz = pytz.timezone('Asia/Seoul')
today_str = datetime.now(seoul_tz).strftime('%Y-%m-%d')
url = f"https://production.dataviz.cnn.io/index/fearandgreed/graphdata/{today_str}"

scraper = cloudscraper.create_scraper()

try:
    res = scraper.get(url, timeout=10)
    if res.status_code != 200:
        # 실패 시 기본 URL로 재시도
        url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
        res = scraper.get(url, timeout=10)

    data = res.json()
    score = round(data['fear_and_greed']['score'])
    rating = data['fear_and_greed']['rating']

    result = {"score": score, "rating": rating}

    # JSON 파일로 덮어쓰기
    with open('fg_data.json', 'w') as f:
        json.dump(result, f)

    print(f"Success: {score} ({rating})")
except Exception as e:
    print(f"Error: {e}")
