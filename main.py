from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import io
import traceback
from yt_downloader.yt_download import download_youtube_video
from facebook_Downloader.fb_downloader import download_facebook_video
from Insta_downloader.insta import download_instagram_video
from Tiktok_downloader.tiktok import download_tiktok_video
from snapchat_download.snapchat import download_snapchat_video

app = FastAPI()

class Item(BaseModel):
    url: str

@app.post("/yt_download/")
def download_yt(item: Item):
    try:
        video_bytes = download_youtube_video(item.url)
        return StreamingResponse(
            io.BytesIO(video_bytes),
            media_type="video/mp4",
            headers={"Content-Disposition": "attachment; filename=video.mp4"}
        )
    except Exception as e:
        print(f"Error: {traceback.format_exc()}")
        return {"error": str(e)}
    
@app.post("/fb_download/")
def download_fb(item: Item):
    try:
        video_bytes = download_facebook_video(item.url)
        return StreamingResponse(
            io.BytesIO(video_bytes),
            media_type="video/mp4",
            headers={"Content-Disposition": "attachment; filename=video.mp4"}
        )
    except Exception as e:
        print(f"Error: {traceback.format_exc()}")
        return {"error": str(e)}
        
@app.post("/insta_download/")
def download_insta(item: Item):
    try:
        video_bytes = download_instagram_video(item.url)
        return StreamingResponse(
            io.BytesIO(video_bytes),
            media_type="video/mp4",
            headers={"Content-Disposition": "attachment; filename=video.mp4"}
        )
    except Exception as e:
        print(f"Error: {traceback.format_exc()}")
        return {"error": str(e)}
        
@app.post("/tiktok_download/")
def download_tiktok(item: Item):
    try:
        video_bytes = download_tiktok_video(item.url)
        return StreamingResponse(
            io.BytesIO(video_bytes),
            media_type="video/mp4",
            headers={"Content-Disposition": "attachment; filename=video.mp4"}
        )
    except Exception as e:
        print(f"Error: {traceback.format_exc()}")
        return {"error": str(e)}

@app.post("/snapchat_download/")
def download_snapchat(item: Item):
    try:
        video_bytes = download_snapchat_video(item.url)
        return StreamingResponse(
            io.BytesIO(video_bytes),
            media_type="video/mp4",
            headers={"Content-Disposition": "attachment; filename=video.mp4"}
        )
    except Exception as e:
        print(f"Error: {traceback.format_exc()}")
        return {"error": str(e)}

@app.get("/")
def root():
    return {
        "message": "Video Downloader API - Stream-on-Demand",
        "endpoints": {
            "/yt_download/": "Download YouTube video (streams directly)",
            "/fb_download/": "Download Facebook video (streams directly)",
            "/insta_download/": "Download Instagram video (streams directly)",
            "/tiktok_download/": "Download TikTok video (streams directly)",
            "/snapchat_download/": "Download Snapchat video (streams directly)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)