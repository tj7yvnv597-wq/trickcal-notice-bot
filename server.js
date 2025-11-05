import express from "express";
import { getLatestNotices } from "./crawler.js";

const app = express();
app.use(express.json());

// 카카오 오픈빌더 webhook
app.post("/kakao", async (req, res) => {
  const userRequest = req.body.userRequest?.utterance || "";
  console.log("사용자 요청:", userRequest);

  if (userRequest.includes("업데이트") || userRequest.includes("공지")) {
    const notices = await getLatestNotices(3);
    const msg = notices.length
      ? notices.map((n, i) => `${i + 1}. ${n.title}\n${n.url}`).join("\n\n")
      : "현재 새 공지를 불러올 수 없습니다.";

    return res.json({
      version: "2.0",
      template: {
        outputs: [
          {
            simpleText: {
              text: `📢 트릭컬 리버스 최신 공지\n\n${msg}`,
            },
          },
        ],
      },
    });
  }

  // 기본 응답
  res.json({
    version: "2.0",
    template: {
      outputs: [
        {
          simpleText: {
            text: "안녕하세요! '트릭컬 업데이트'라고 말하면 최신 공지를 알려드려요 😊",
          },
        },
      ],
    },
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ Server running on port ${PORT}`));
