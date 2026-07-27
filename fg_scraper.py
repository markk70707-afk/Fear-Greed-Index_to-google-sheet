import json
import sys
import cloudscraper

url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"

# 크롬 브라우저 환경 모방
scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://www.cnn.com/markets"
}

try:
    res = scraper.get(url, headers=headers, timeout=15)
    
    if res.status_code != 200:
        print(f"CNN API HTTP Error: {res.status_code}")
        sys.exit(1)

    data = res.json()
    if 'fear_and_greed' not in data:
        print("Response JSON Structure Error")
        sys.exit(1)

    score = round(data['fear_and_greed']['score'])
    rating = data['fear_and_greed']['rating']

    result = {"score": score, "rating": rating}

    with open('fg_data.json', 'w') as f:
        json.dump(result, f)

    print(f"Success: {score} ({rating})")

except Exception as e:
    print(f"Execution Error: {e}")
    sys.exit(1)
