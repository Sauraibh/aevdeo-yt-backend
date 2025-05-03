import yt_dlp
import re

class VideoDownloader:
    def __init__(self, url):
        self.url = url
        self.platform_patterns = {
            'instagram': r'(?:https?:\/\/)?(?:www\.)?instagram\.com',
            'facebook': r'(?:https?:\/\/)?(?:www\.)?(?:fb\.com|facebook\.com)',
            'twitter': r'(?:https?:\/\/)?(?:www\.)?(?:x\.com|twitter\.com)',
            'pinterest': r'(?:https?:\/\/)?(?:www\.)?pinterest\.com',
            'threads': r'(?:https?:\/\/)?(?:www\.)?threads\.net'
        }

    def identify_platform(self):
        for platform, pattern in self.platform_patterns.items():
            if re.match(pattern, self.url):
                return platform
        return 'unknown'

    def get_video_info(self):
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4',
            'extract_flat': False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                return info
        except Exception as e:
            print(f"Error fetching video info: {str(e)}")
            return None