from flask import Flask, jsonify, request
from downloader.downloader import VideoDownloader
from utils.helpers import validate_url
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'message': 'AEVDEO Backend API is live!'})

@app.route('/api/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400

        url = data['url']
        if not validate_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400

        downloader = VideoDownloader(url)
        video_info = downloader.get_video_info()

        if not video_info:
            return jsonify({'error': 'Failed to fetch video information'}), 404

        response = {
            'status': 'success',
            'platform': downloader.identify_platform(),
            'title': video_info.get('title', 'Unknown'),
            'thumbnail': video_info.get('thumbnail', ''),
            'formats': [
                {
                    'quality': f.get('format_note', 'unknown'),
                    'url': f.get('url'),
                    'filesize': f.get('filesize', 0),
                    'ext': f.get('ext', 'mp4')
                } for f in video_info.get('formats', [])
                if f.get('url') and f.get('vcodec') != 'none'
            ]
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)