
from flask import Flask, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "AEVDEO yt-dlp backend is live!"

@app.route("/fetch", methods=["POST"])
def fetch():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        temp_id = str(uuid.uuid4())
        output_path = f"/tmp/{temp_id}.%(ext)s"

        cmd = [
            "yt-dlp",
            "--skip-download",
            "--print", "title",
            "--print", "thumbnail",
            "--print", "url",
            "-o", output_path,
            url
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout.strip().split("\n")

        if len(output) < 3:
            return jsonify({"error": "Could not extract video info"}), 500

        return jsonify({
            "title": output[0],
            "thumbnail": output[1],
            "downloadLinks": [
                {"url": output[2], "quality": "default"}
            ]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
