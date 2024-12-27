import os
import logging
import requests
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class YouTubeVideoFetcher:
    """Class để xử lý việc lấy video từ một channel YouTube."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'X-RapidAPI-Key': api_key,
            'X-RapidAPI-Host': "youtube-media-downloader.p.rapidapi.com"
        }

    def get_channel_videos(self, channel_id: str) -> List[Dict]:
        """
        Lấy danh sách video từ Channel ID sử dụng API RapidAPI.
        """
        try:
            url = f"https://youtube-media-downloader.p.rapidapi.com/v2/channel/videos"
            params = {
                "channelId": channel_id,
                "type": "videos",
                "sortBy": "newest"
            }
            
            logger.debug(f"Gọi API RapidAPI với URL: {url}")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            data = response.json()
            videos = data.get("videos", [])
            logger.debug(f"Tìm thấy {len(videos)} video.")

            return [
                {
                    'url': f"https://www.youtube.com/watch?v={video['videoId']}",
                    'title': video.get('title', ''),
                    'videoId': video.get('videoId', '')
                }
                for video in videos
                if video.get('videoId')
            ]

        except Exception as e:
            logger.exception(f"Lỗi trong hàm get_channel_videos: {str(e)}")
            return []
