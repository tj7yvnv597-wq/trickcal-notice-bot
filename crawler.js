import axios from "axios";
import * as cheerio from "cheerio";

// 트릭컬 리버스 업데이트 공지 카테고리 주소
const TARGET_URL = "https://cafe.naver.com/ArticleList.nhn?search.clubid=30131231&search.menuid=67&search.boardtype=L";

export async function getLatestNotices(limit = 3) {
  try {
    const { data } = await axios.get(TARGET_URL, {
      headers: {
        "User-Agent": "Mozilla/5.0",
      },
    });

    const $ = cheerio.load(data);

    // 게시글 목록 테이블에서 제목/링크 추출
    const notices = [];
    $("a.article").each((i, el) => {
      if (i >= limit) return false;
      const title = $(el).text().trim();
      const link = $(el).attr("href");
      if (title && link) {
        notices.push({
          title,
          url: `https://cafe.naver.com${link}`,
        });
      }
    });

    return notices;
  } catch (err) {
    console.error("공지 크롤링 실패:", err);
    return [];
  }
}
