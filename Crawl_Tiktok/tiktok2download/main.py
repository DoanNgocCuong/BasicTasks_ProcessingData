import os
from pathlib import Path
from dotenv import load_dotenv
from tiktok2download.def_getListVideosTiktok import fetch_tiktok_videos
from utils_saveListVideosToExcel import save_videos_to_excel
from tiktok2download.def_Tiktok2VideoDownload import TikTokDownloader

def setup_environment():
    """Setup environment variables and directories"""
    env_path = Path(__file__).parent / '.env'
    load_dotenv(dotenv_path=env_path)
    
    api_key = os.getenv("TIKTOK_API_KEY")
    if not api_key:
        raise ValueError("Error: TIKTOK_API_KEY environment variable not set")
    
    return api_key

def process_videos(username: str, max_videos: int = 30):
    """Main process to fetch, save and download videos"""
    try:
        # Setup
        api_key = setup_environment()
        output_dir = Path(__file__).parent / "output"
        
        print(f"\nProcessing TikTok videos for user: {username}")
        print(f"Maximum videos to process: {max_videos}")
        
        # Step 1: Fetch videos list
        videos = fetch_tiktok_videos(username, api_key, max_videos)
        if not videos:
            print("No videos found")
            return
        
        # Step 2: Save to Excel
        excel_path = save_videos_to_excel(
            videos, 
            output_dir=str(output_dir),
            filename=f"{username}_videos.xlsx"
        )
        
        if not excel_path:
            print("Failed to save Excel file")
            return
            
        # Step 3: Download videos
        downloader = TikTokDownloader(api_key)
        for video in videos:
            video_id = video['id']
            filename = f"{username}_{video_id}.mp4"
            print(f"\nDownloading video {video_id}...")
            downloader.download_video(username, video_id, filename)
            
        print("\nProcess completed successfully!")
        
    except Exception as e:
        print(f"\nError in main process: {str(e)}")
        raise

if __name__ == "__main__":
    # Configuration
    USERNAME = "moxierobot"  # Change this to target username
    MAX_VIDEOS = 30          # Maximum number of videos to process
    
    process_videos(USERNAME, MAX_VIDEOS)