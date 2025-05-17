const express = require('express');
const puppeteer = require('puppeteer');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

app.post('/api/download', async (req, res) => {
  const { url } = req.body;
  if (!url) return res.status(400).json({ error: 'Missing URL' });

  try {
    const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox']
    });
    const page = await browser.newPage();

    if (process.env.COOKIE_STRING) {
      const cookies = JSON.parse(process.env.COOKIE_STRING);
      await page.setCookie(...cookies);
    }

    await page.goto(url, { waitUntil: 'networkidle2' });

    const videoSrc = await page.evaluate(() => {
      const video = document.querySelector('video');
      return video ? video.src : null;
    });

    await browser.close();

    if (videoSrc) {
      res.json({ downloadLinks: [{ url: videoSrc, quality: "default" }] });
    } else {
      res.status(404).json({ message: "No video found" });
    }
  } catch (err) {
    res.status(500).json({ error: err.toString() });
  }
});

app.get('/', (req, res) => {
  res.send('Aevdeo Puppeteer API is live.');
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`Running on ${PORT}`));