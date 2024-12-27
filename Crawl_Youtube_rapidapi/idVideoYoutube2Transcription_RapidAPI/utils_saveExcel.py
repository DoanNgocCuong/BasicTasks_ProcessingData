import pandas as pd
import logging
import os
from typing import Dict
from shutil import copyfile

logger = logging.getLogger(__name__)

class TranscriptExcelSaver:
    """Class để lưu transcript vào file Excel."""

    def __init__(self, output_dir: str = "output"):
        """
        Khởi tạo TranscriptExcelSaver với thư mục output.
        
        Args:
            output_dir (str): Đường dẫn đến thư mục output
        """
        self.output_dir = output_dir
        self.output_file = "transcript_output.xlsx"
        self.output_path = os.path.join(output_dir, self.output_file)
        self._ensure_output_dir()

    def _ensure_output_dir(self) -> None:
        """Tạo thư mục output nếu chưa tồn tại."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"Đã tạo thư mục output: {self.output_dir}")

    def save_transcript(self, transcript_data: Dict, video_info: Dict, input_file: str) -> str:
        """
        Lưu transcript vào file Excel.
        
        Args:
            transcript_data (Dict): Dữ liệu transcript
            video_info (Dict): Thông tin video
            input_file (str): Đường dẫn file Excel input
            
        Returns:
            str: Đường dẫn đến file Excel đã tạo
        """
        try:
            # Copy file input nếu file output chưa tồn tại
            if not os.path.exists(self.output_path):
                copyfile(input_file, self.output_path)
                logger.info(f"Đã tạo file output từ file input: {self.output_path}")

            # Đọc file Excel hiện tại
            df = pd.read_excel(self.output_path)
            
            # Tìm và cập nhật dòng chứa video_id tương ứng
            video_id = video_info['videoId']
            mask = df['ID video'] == video_id
            
            if mask.any():
                # Thêm cột transcript nếu chưa có
                if 'transcript' not in df.columns:
                    df['transcript'] = None
                    
                df.loc[mask, 'transcript'] = transcript_data['transcript']
                
                # Lưu lại file Excel
                df.to_excel(self.output_path, index=False)
                logger.info(f"Đã cập nhật transcript cho video {video_id}")
                
                return self.output_path
            else:
                logger.error(f"Không tìm thấy video {video_id} trong file Excel")
                return ""

        except Exception as e:
            logger.exception(f"Lỗi khi lưu transcript vào Excel: {str(e)}")
            return ""
