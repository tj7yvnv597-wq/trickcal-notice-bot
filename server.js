import express from "express";
import { getLatestNotices } from "./crawler.js";

const app = express();
app.use(express.json());

app.get("/", (req, res) => {
  res.send("✅ Trickcal Update Bot is running.");
});

// 카카오 i 오픈빌더 Webhook 엔드포인트
app.post("/kakao", async (req, res) => {
  const utter = req.body.userRequest?.utterance || "";
  console.log("📥 User Request:", utter);

  if (utter.includes("공지") || utter.includes("업데이트")) {
    const notices = await getLatestNotices(3);
    const message = notices.length
      ? notices.map((n, i) => `${i + 1}. ${n.title}\n${n.url}`).join("\n\n")
      : "현재 새 공지를 불러올 수 없습니다.";

    return res.json({
      version: "2.0",
      template: {
        outputs: [
          {
            simpleText: {
              text: `📢 트릭컬 리버스 최신 공지\n\n${message}`,
            },
          },
        ],
      },
    });
  }

  return res.json({
    version: "2.0",
    template: {
      outputs: [
        {
          simpleText: {
            text: "안녕하세요! 😊\n'트릭컬 업데이트' 또는 '공지'라고 입력하면 최신 소식을 알려드릴게요.",
          },
        },
      ],
    },
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
