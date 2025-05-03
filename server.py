from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url', '')
    return jsonify({
        "status": "success",
        "platform": "instagram",
        "url": url,
        "thumbnail": "https://example.com/sample_thumbnail.jpg",
        "videos": [
            {"quality": "480p", "link": "https://example.com/video_480p.mp4"},
            {"quality": "720p", "link": "https://example.com/video_720p.mp4"}
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)