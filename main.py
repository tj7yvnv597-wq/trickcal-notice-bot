from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_notice():
    url = "https://trickcal.com/news/notice"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    first_notice = soup.select_one(".board-list-wrap a")
    title = first_notice.select_one(".tit").text.strip()
    link = "https://trickcal.com" + first_notice.get("href")

    return f"📢 트릭컬 최신 공지\n\n{title}\n{link}"

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
