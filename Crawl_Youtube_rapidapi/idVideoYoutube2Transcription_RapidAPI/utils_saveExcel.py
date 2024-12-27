import pandas as pd
import logging
from datetime import datetime
import os
from typing import List, Dict

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
        self._ensure_output_dir()

    def _ensure_output_dir(self) -> None:
        """Tạo thư mục output nếu chưa tồn tại."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"Đã tạo thư mục output: {self.output_dir}")

    def _generate_filename(self, video_id: str) -> str:
        """Tạo tên file Excel với timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"transcript_{video_id}_{timestamp}.xlsx"

    def save_transcript(self, transcript_data: Dict, video_info: Dict) -> str:
        """
        Lưu transcript vào file Excel.
        
        Args:
            transcript_data (Dict): Dữ liệu transcript
            video_info (Dict): Thông tin video
            
        Returns:
            str: Đường dẫn đến file Excel đã tạo
        """
        try:
            # Tạo DataFrame từ transcript
            df = pd.DataFrame(transcript_data['transcript'])
            
            # Thêm thông tin video
            metadata = pd.DataFrame([{
                'Video Title': video_info['title'],
                'Video URL': video_info['url'],
                'Video ID': video_info['videoId']
            }])

            # Tạo tên file và đường dẫn
            filename = self._generate_filename(video_info['videoId'])
            filepath = os.path.join(self.output_dir, filename)

            # Lưu vào Excel với nhiều sheet
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                metadata.to_excel(writer, sheet_name='Video Info', index=False)
                df.to_excel(writer, sheet_name='Transcript', index=False)
                
                # Tự động điều chỉnh độ rộng cột
                for sheet_name in writer.sheets:
                    worksheet = writer.sheets[sheet_name]
                    for idx, col in enumerate(df.columns):
                        max_length = max(
                            df[col].astype(str).apply(len).max(),
                            len(col)
                        )
                        worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2

            logger.info(f"Đã lưu transcript vào file: {filepath}")
            return filepath

        except Exception as e:
            logger.exception(f"Lỗi khi lưu transcript vào Excel: {str(e)}")
            return ""
