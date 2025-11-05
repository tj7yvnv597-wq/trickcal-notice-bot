from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_notice():
    url = "https://game.naver.com/lounge/Trickcal/board/11"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 공지 제목 & 링크 선택
    item = soup.select_one(".title_area .title")

    if not item:
        return "⚠️ 공지를 불러올 수 없습니다."

    title = item.get_text(strip=True)
    link = "https://game.naver.com" + item["href"]

    return f"📢 트릭컬 최신 공지\n\n{title}\n{link}"

@app.route("/", methods=["POST"])
def skill():
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": get_notice()
                    }
                }
            ]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
