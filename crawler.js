import axios from "axios";
import * as cheerio from "cheerio";

// 트릭컬 리버스 업데이트 공지 카테고리 URL
const TARGET_URL =
  "https://cafe.naver.com/ArticleList.nhn?search.clubid=30131231&search.menuid=67&search.boardtype=L";

/**
 * 최신 공지글 가져오기
 * @param {number} limit - 가져올 글 개수
 */
export async function getLatestNotices(limit = 3) {
  try {
    const { data } = await axios.get(TARGET_URL, {
      headers: { "User-Agent": "Mozilla/5.0" },
    });

    const $ = cheerio.load(data);
    const notices = [];

    $("a.article").each((i, el) => {
      if (i >= limit) return false;
      const title = $(el).text().trim();
      const href = $(el).attr("href");
      if (title && href) {
        notices.push({
          title,
          url: `https://cafe.naver.com${href}`,
        });
      }
    });

    return notices;
  } catch (err) {
    console.error("공지 크롤링 실패:", err.message);
    return [];
  }
}
