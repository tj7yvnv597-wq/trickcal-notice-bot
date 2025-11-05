from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_notice():
    url = "https://game.naver.com/lounge/Trickcal/board/11"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    titles = soup.select(".title_area .title")
    
    if not titles:
        return "⚠️ 공지를 불러올 수 없습니다."

    first_title = titles[0].get_text(strip=True)
    first_link = "https://game.naver.com" + titles[0]["href"]

    return f"📢 트릭컬 최신 공지\n\n{first_title}\n{first_link}"

@app.route("/", methods=["POST"])
def skill():
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [


