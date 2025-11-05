import os
import requests
from flask import Flask, jsonify, request
# 웹 크롤링을 위한 라이브러리 (pip install beautifulsoup4)
from bs4 import BeautifulSoup 

app = Flask(__name__)

# --- 설정 ---
# '트릭컬 리바이브 공식 카페' 업데이트 게시판 URL (실제 URL로 변경 필요)
CAFE_UPDATE_URL = "실제_업데이트_게시판_URL_입력" 
# Render 배포 시 환경 변수로 설정 가능 (옵션)
# CAFE_UPDATE_URL = os.getenv("CAFE_URL", "기본_URL") 
# -----------------

def get_latest_cafe_updates():
    """
    네이버 카페에서 최신 업데이트 내용을 크롤링하여 가져오는 함수입니다.
    이 함수는 예시이며, 실제 동작을 위해서는 네이버 카페 HTML 구조에 맞춰 
    BeautifulSoup 로직을 완성해야 합니다.
    """
    try:
        # 네이버 카페는 로그인 및 접근 권한 문제로 요청이 실패할 수 있습니다.
        # 실제 구현 시 세션 유지 또는 Selenium 등의 고급 크롤링 기술이 필요할 수 있습니다.
        response = requests.get(CAFE_UPDATE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status() # HTTP 오류 발생 시 예외 처리

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ---  ---
        
        # TODO: 실제 카페 HTML 구조를 분석하여 최신 글 제목, 링크 등을 파싱하는 로직 구현
        # 예시: 최신 5개 글을 가져온다고 가정
        
        # 'a' 태그 중 글 목록에 해당하는 요소를 찾아 파싱 (이 부분은 카페마다 다릅니다)
        # 예시: (가상의 클래스 이름 'latest_post' 사용)
        posts = soup.select('.latest_post') 
        
        updates = []
        for i, post in enumerate(posts[:5]):
            title = post.text.strip()
            # 네이버 카페 게시물 링크는 프레임 내부에 있어, 실제 링크를 추출하는 로직도 복잡할 수 있습니다.
            link = "링크 추출 로직 필요" 
            updates.append(f"{i+1}. {title}")
        
        if updates:
            return "트릭컬 리바이브 공식 카페 최신 업데이트:\n" + "\n".join(updates)
        else:
            return "죄송합니다. 현재 최신 업데이트 정보를 가져올 수 없습니다. (크롤링 실패 또는 게시글 없음)"

    except requests.exceptions.RequestException as e:
        print(f"Error during web request: {e}")
        return "죄송합니다. 서버 통신에 문제가 발생했습니다."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "죄송합니다. 처리 중 예상치 못한 오류가 발생했습니다."

@app.route('/api/update', methods=['POST'])
def handle_kakao_skill():
    """
    카카오 i 오픈빌더 스킬 서버의 요청을 처리하는 엔드포인트입니다.
    """
    try:
        # 카카오톡 챗봇 요청 본문을 받음 (사용자 발화, 파라미터 등 포함)
        req = request.get_json()
        print("Received Kakao Request:", req)
        
        # 업데이트 내용을 가져옴
        update_text = get_latest_cafe_updates()
        
        # 카카오 i 오픈빌더 SimpleText 응답 형식에 맞춤
        response_data = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": update_text
                        }
                    }
                ]
            }
        }
        
        return jsonify(response_data)

    except Exception as e:
        # 오류 발생 시 기본 오류 메시지 응답
        print(f"Error processing request: {e}")
        return jsonify({
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "죄송합니다. 스킬 처리 중 내부 오류가 발생했습니다."
                        }
                    }
                ]
            }
        }), 500

# 서버 실행 (Render 배포 시 필요 없음, Gunicorn 등이 사용됨)
if __name__ == '__main__':
    # 로컬 테스트용
    app.run(host='0.0.0.0', port=5000)
