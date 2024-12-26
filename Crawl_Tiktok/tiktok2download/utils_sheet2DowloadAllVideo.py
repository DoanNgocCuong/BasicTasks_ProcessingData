import pandas as pd
from tiktok2download.def_Tiktok2VideoDownload import TikTokDownloader
import os
from dotenv import load_dotenv

load_dotenv()

def download_all_videos_from_sheet(sheet_path: str):
    """Download all videos from a sheet
    
    Sử dụng hàm @Cuong_Tiktok2VideoDownload.py để download video
    
    """
    
    # Read the Excel file
    df = pd.read_excel(sheet_path)

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        video_id = row['Video ID']
        video_url = row['URL']
        
        # Extract username from the URL
        username = video_url.split('@')[1].split('/')[0]
        
        # Create a downloader instance
        tiktok_api_key = os.getenv("TIKTOK_API_KEY")
        downloader = TikTokDownloader(username, video_id, tiktok_api_key)
        
        # Download the video
        filename = f"{username}_{video_id}.mp4"
        downloader.download_video(filename)

# Sử dụng hàm này
download_all_videos_from_sheet("MoxieRobot_Videos.xlsx")
