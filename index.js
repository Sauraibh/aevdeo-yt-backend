 const express = require("express");
const cors = require("cors");
const fetch = require("node-fetch");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors({ origin: true }));
app.use(express.json());

app.get("/", (req, res) => {
  res.send("AEVDEO Real Instagram Backend is live!");
});

app.post("/fetch", async (req, res) => {
  const { url } = req.body;

  if (!url || !url.includes("instagram.com")) {
    return res.status(400).json({ error: "Invalid or missing Instagram URL." });
  }

  try {
    const apiResponse = await fetch(`https://api.vevioz.com/api/button/instagram?url=${encodeURIComponent(url)}`);
    const html = await apiResponse.text();

    const videoMatch = html.match(/href="(https:\\/\\/[^"]+\\.mp4)"/);
    const thumbMatch = html.match(/<img src="(https:\\/\\/[^"]+)" alt=/);

    if (!videoMatch) {
      return res.json({ message: "Could not extract video. Try another link." });
    }

    res.json({
      platform: "Instagram",
      thumbnail: thumbMatch ? thumbMatch[1] : null,
      downloadLinks: [
        {
          url: videoMatch[1],
          quality: "Default"
        }
      ]
    });

  } catch (error) {
    res.status(500).json({ error: "Failed to fetch video data." });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});