from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_notice():
    url = "https://trickcal.yostar.kr/news"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    # 공지 리스트 가져오기 (현재 페이지 구조 기준)
    notice = soup.select_one(".news_list li a")
    if notice is None:
        return "⚠ 공지 데이터를 가져오지 못했습니다."

    title = notice.select_one(".title").text.strip()
    date = notice.select_one(".date").text.strip()
    link = "https://trickcal.yostar.kr" + notice.get("href")

    return f"[최근 공지]\n{title}\n({date})\n\n바로가기: {link}"

@app.route("/", methods=["POST"])
def skill():
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": get_notice()}}
            ]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
