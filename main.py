from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_notice():
    url = "https://trickcal.yostar.kr/news.rss"
    res = requests.get(url, timeout=5)
    soup = BeautifulSoup(res.text, "xml")

    first = soup.find("item")
    if first is None:
        return "⚠ 공지 데이터를 불러오지 못했습니다."

    title = first.title.text.strip()
    link = first.link.text.strip()
    date = first.pubDate.text.strip()

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

