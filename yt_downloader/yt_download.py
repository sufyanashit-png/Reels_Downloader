import tempfile
import os
import sys
import shutil
from yt_dlp import YoutubeDL

# Modern user agent for YouTube requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def download_youtube_video(url):
    temp_dir = tempfile.mkdtemp()
    temp_file = None
    try:
        # Convert Shorts URL to regular YouTube URL
        if 'youtube.com/shorts/' in url:
            video_id = url.split('/shorts/')[1].split('?')[0]
            url = f'https://www.youtube.com/watch?v={video_id}'
        
        # Configure yt_dlp without requiring browser cookies
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'user_agent': USER_AGENT,
            'socket_timeout': 30,
            'http_headers': {
                'User-Agent': USER_AGENT,
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Referer': 'https://www.youtube.com/',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['web_embedded', 'web'],  # Use web client instead of android
                    'skip': ['hls'],  # Skip age-gate bypass attempts
                }
            },
            'socket_timeout': 30,
            'retries': 5,  # Retry up to 5 times on network failure
            'fragment_retries': 5,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            temp_file = ydl.prepare_filename(info)
        
        if not os.path.exists(temp_file):
            raise Exception("Video file was not downloaded successfully")
        
        with open(temp_file, 'rb') as f:
            video_bytes = f.read()
        
        return video_bytes
        
    except Exception as e:
        raise Exception(f"YouTube download failed: {str(e)}")
    finally:
        # Cleanup temporary files and directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        url = input("Enter YouTube video URL: ")
    else:
        url = sys.argv[1]

    result = download_youtube_video(url)
    print(result)