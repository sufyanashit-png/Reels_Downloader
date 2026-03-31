import tempfile
import glob
import os
from pytube import YouTube

def download_youtube_video(url):
    temp_dir = tempfile.mkdtemp()
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        
        if not stream:
            stream = yt.streams.get_highest_resolution()
        
        output_file = stream.download(output_path=temp_dir)
        
        with open(output_file, 'rb') as f:
            video_bytes = f.read()
        
        os.remove(output_file)
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