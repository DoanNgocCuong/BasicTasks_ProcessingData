



Được, tôi sẽ tạo file main.py để điều phối toàn bộ quy trình:

```python:tiktok2download/main.py
from pathlib import Path
from dotenv import load_dotenv
import os
from def_getListVideosTiktok import fetch_tiktok_videos
from utils_saveListVideosToExcel import save_videos_to_excel
from utils_AllVideoToTranscription1Role import process_all_videos

def setup_environment():
    """Setup environment variables and directories"""
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
    
    api_key = os.getenv("TIKTOK_API_KEY")
    if not api_key:
        raise ValueError("Error: TIKTOK_API_KEY environment variable not set")
    
    return api_key

def main():
    """Main process to fetch videos, save to Excel, and transcribe"""
    try:
        # Configuration
        USERNAME = "moxierobot"
        MAX_VIDEOS = 30
        
        # Setup
        api_key = setup_environment()
        current_dir = Path(__file__).parent
        excel_output_dir = current_dir / "excel_output"
        excel_file = "MoxieRobot_Videos.xlsx"
        
        print(f"\nStarting process for user: {USERNAME}")
        print(f"Maximum videos to process: {MAX_VIDEOS}")
        
        # Step 1: Fetch videos list
        print("\nFetching videos list...")
        videos = fetch_tiktok_videos(USERNAME, api_key, MAX_VIDEOS)
        if not videos:
            print("No videos found")
            return
        
        # Step 2: Save to Excel
        print("\nSaving to Excel...")
        excel_path = save_videos_to_excel(
            videos, 
            output_dir=str(excel_output_dir),
            filename=excel_file
        )
        
        if not excel_path:
            print("Failed to save Excel file")
            return
            
        # Step 3: Process transcriptions
        print("\nProcessing video transcriptions...")
        process_all_videos()
        
        print("\nProcess completed successfully!")
        
    except Exception as e:
        print(f"\nError in main process: {str(e)}")
        raise

if __name__ == "__main__":
    main()
```


File main.py này sẽ:

1. Setup môi trường và load API keys
2. Fetch danh sách video từ TikTok
3. Lưu thông tin video vào Excel
4. Xử lý transcription cho tất cả video đã tải về

Cấu trúc thư mục sẽ như sau:
```
tiktok2download/
├── main.py
├── def_getListVideosTiktok.py
├── utils_saveListVideosToExcel.py
├── utils_AllVideoToTranscription1Role.py
├── excel_output/
│   └── MoxieRobot_Videos.xlsx
└── video_downloaded/
    └── (downloaded videos)
```

Để chạy toàn bộ quy trình, chỉ cần chạy:
```bash
python main.py
```
