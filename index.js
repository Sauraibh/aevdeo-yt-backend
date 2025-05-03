
const express = require("express");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors({ origin: true }));
app.use(express.json());

app.post("/fetch", async (req, res) => {
  const { url } = req.body;

  if (!url) {
    return res.status(400).json({ error: "URL is required." });
  }

  let platform = "unknown";

  if (url.includes("instagram.com")) platform = "Instagram";
  else if (url.includes("facebook.com") || url.includes("fb.watch")) platform = "Facebook";
  else if (url.includes("x.com") || url.includes("twitter.com")) platform = "X";
  else if (url.includes("pinterest.com")) platform = "Pinterest";
  else if (url.includes("threads.net")) platform = "Threads";

  const downloadLinks = [
    {
      url: "https://example.com/video_720p.mp4",
      quality: "720p",
      platform
    },
    {
      url: "https://example.com/video_480p.mp4",
      quality: "480p",
      platform
    }
  ];

  return res.json({ platform, downloadLinks });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
