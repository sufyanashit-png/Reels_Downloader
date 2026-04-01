import yt_dlp
import sys
import os
import tempfile
import glob
import shutil


def create_cookie_file():
    cookie_data = os.getenv("YOUTUBE_COOKIES")
    cookie_path = "/tmp/cookies.txt"
    if cookie_data:
        with open(cookie_path, "w") as f:
            f.write(cookie_data)
        return cookie_path
    return None


def download_youtube_video(url):
    cookie_file = create_cookie_file()
    temp_dir = tempfile.mkdtemp(dir="/tmp")

    try:
        output_template = os.path.join(temp_dir, "video.%(ext)s")

        options = {
            "quiet": True,
            "no_warnings": True,

            # NEVER use '+' merge syntax — only pick pre-merged single-file formats
            # [vcodec!=none][acodec!=none] = file already has both video AND audio
            "format": (
                "best[ext=mp4][vcodec!=none][acodec!=none]"
                "/best[ext=webm][vcodec!=none][acodec!=none]"
                "/best[vcodec!=none][acodec!=none]"
                "/best"
            ),

            # Prevent yt-dlp from ever trying to merge streams
            "merge_output_format": None,
            "postprocessors": [],

            "cookiefile": cookie_file,
            "socket_timeout": 20,
            "retries": 3,
            "fragment_retries": 3,

            "http_headers": {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept-Language": "en-US,en;q=0.9",
            },

            "outtmpl": output_template,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.extract_info(url, download=True)

        files = glob.glob(os.path.join(temp_dir, "*"))
        if not files:
            raise Exception("No video file was downloaded.")

        video_file = files[0]
        with open(video_file, "rb") as f:
            video_bytes = f.read()

        return video_bytes

    except yt_dlp.utils.DownloadError as e:
        raise Exception(f"yt-dlp error: {str(e)}")

    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        url = input("Enter YouTube video URL: ")
    else:
        url = sys.argv[1]

    result = download_youtube_video(url)
    print(f"Downloaded {len(result)} bytes")