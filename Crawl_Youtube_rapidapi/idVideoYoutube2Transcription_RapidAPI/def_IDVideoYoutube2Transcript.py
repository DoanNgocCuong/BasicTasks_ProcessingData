import requests
import logging
from typing import Dict, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class YouTubeTranscriptFetcher:
    """Class để lấy transcript từ video YouTube."""

    def __init__(self):
        self.api_key = os.getenv('RAPID_API_KEY')
        self.headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': 'youtube-media-downloader.p.rapidapi.com'
        }

    def get_transcript(self, video_id: str) -> Optional[Dict]:
        """
        Lấy transcript cho một video YouTube.
        
        Args:
            video_id (str): ID của video YouTube
            
        Returns:
            Optional[Dict]: Transcript của video hoặc None nếu có lỗi
        """
        try:
            url = "https://youtube-media-downloader.p.rapidapi.com/v2/video/subtitles"
            params = {"videoId": video_id}

            logger.debug(f"Gọi API để lấy transcript cho video ID: {video_id}")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            data = response.json()
            
            if not data.get("status"):
                logger.error(f"API trả về lỗi: {data.get('errorId', 'Unknown error')}")
                return None

            return {
                'transcript': data.get('subtitles', []),
                'status': 'success'
            }

        except requests.exceptions.RequestException as e:
            logger.exception(f"Lỗi khi lấy transcript: {str(e)}")
            return None
        except Exception as e:
            logger.exception(f"Lỗi không xác định: {str(e)}")
            return None
