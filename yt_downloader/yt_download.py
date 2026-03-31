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
            'format': 'best',
            'socket_timeout': 30,
            'retries': 5,
            'fragment_retries': 5,
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
        url = input("Enter YouTube video URL: ")
    else:
        url = sys.argv[1]

    result = download_youtube_video(url)
    print(result)