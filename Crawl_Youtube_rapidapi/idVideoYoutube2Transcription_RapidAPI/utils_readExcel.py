import pandas as pd
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class ExcelReader:
    """Class để đọc dữ liệu từ file Excel."""

    @staticmethod
    def read_videos_from_excel(filepath: str) -> List[Dict]:
        """
        Đọc danh sách video từ file Excel.
        
        Args:
            filepath (str): Đường dẫn đến file Excel
            
        Returns:
            List[Dict]: Danh sách các video với thông tin url và title
        """
        try:
            # Đọc file Excel
            df = pd.read_excel(filepath)
            
            # Kiểm tra các cột cần thiết
            required_columns = ['Đường dẫn video', 'Tiêu đề', 'ID video']
            if not all(col in df.columns for col in required_columns):
                logger.error("File Excel không có đủ các cột cần thiết")
                return []
            
            # Chuyển DataFrame thành list of dictionaries
            videos = []
            for _, row in df.iterrows():
                video = {
                    'url': row['Đường dẫn video'],
                    'title': row['Tiêu đề'],
                    'videoId': row['ID video']
                }
                videos.append(video)
            
            logger.info(f"Đã đọc thành công {len(videos)} video từ file Excel")
            return videos
            
        except Exception as e:
            logger.exception(f"Lỗi khi đọc file Excel: {str(e)}")
            return []
