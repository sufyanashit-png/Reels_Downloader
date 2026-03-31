import yt_dlp
import os
import sys
import tempfile
import glob

def download_tiktok_video(url):
    temp_dir = tempfile.mkdtemp()
    try:
        output_template = os.path.join(temp_dir, 'video.%(ext)s')

        options = {
            'quiet': True,
            'no_warnings': True,
            'format': 'bestvideo+bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegConcat',
                'only_multi_video': False,
                'when': 'playlist',
            }, {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://www.tiktok.com/',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            },
            'socket_timeout': 30,
            'retries': 5,
            'fragment_retries': 5,
            'merge_output_format': 'mp4',
            'outtmpl': output_template
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
        url = input("Enter TikTok video URL: ")
    else:
        url = sys.argv[1]

    result = download_tiktok_video(url)
    print(result)