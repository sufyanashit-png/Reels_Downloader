import yt_dlp
import sys
import os
import tempfile
import glob

def download_youtube_video(url):
    temp_dir = tempfile.mkdtemp()
    try:
        output_template = os.path.join(temp_dir, 'video.%(ext)s')
        
        options = {
            'quiet': True,
            'no_warnings': True,
            'format': 'best[ext=mp4]/best',
            'socket_timeout': 30,
            'retries': 3,
            'fragment_retries': 3,
            'outtmpl': output_template,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['web', 'mweb']
                }
            }
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.extract_info(url, download=True)
        
        files = glob.glob(os.path.join(temp_dir, '*'))
        if not files:
            raise Exception("No video file downloaded")
        
        video_file = files[0]
        with open(video_file, 'rb') as f:
            video_bytes = f.read()
        
        os.remove(video_file)
        os.rmdir(temp_dir)
        
        return video_bytes
    except Exception as e:
        import shutil
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        raise e

if __name__ == "__main__":
    if len(sys.argv) < 2:
        url = input("Enter YouTube video URL: ")
    else:
        url = sys.argv[1]

    result = download_youtube_video(url)
    print(result)