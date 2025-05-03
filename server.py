from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Aevdeo Backend is Live!"

@app.route("/api/download", methods=["POST"])
def download_video():
    data = request.get_json()
    url = data.get("videoUrl")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'force_generic_extractor': False,
        'extract_flat': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            results = []

            for f in formats:
                if f.get("url") and f.get("format_note") and f.get("ext") == "mp4":
                    results.append({
                        "url": f["url"],
                        "quality": f["format_note"]
                    })

            return jsonify({"downloadLinks": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500