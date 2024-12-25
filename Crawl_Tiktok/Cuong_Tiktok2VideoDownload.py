import requests

class TikTokDownloader:
    def __init__(self, author_uniqueid, video_id, tiktok_api_key):
        self.author_uniqueid = author_uniqueid
        self.video_id = video_id
        self.tiktok_api_key = tiktok_api_key
        self.tiktok_api_url = "https://tiktok-api23.p.rapidapi.com/api/download/video"
        self.tiktok_api_host = "tiktok-api23.p.rapidapi.com"

    def get_download_link(self):
        """Get the video download link from TikTok API."""
        tiktok_url = f"https://www.tiktok.com/@{self.author_uniqueid}/video/{self.video_id}"
        headers = {
            "x-rapidapi-key": self.tiktok_api_key,
            "x-rapidapi-host": self.tiktok_api_host
        }
        params = {"url": tiktok_url}
        
        try:
            response = requests.get(self.tiktok_api_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("play")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching download link: {e}")
            return None

    def download_video(self, save_path):
        """Download the video and save it locally."""
        download_link = self.get_download_link()
        if not download_link:
            print("Failed to retrieve download link.")
            return
        
        try:
            print(f"Downloading video from: {download_link}")
            response = requests.get(download_link, stream=True)
            response.raise_for_status()
            with open(save_path, "wb") as video_file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        video_file.write(chunk)
            print(f"Video saved to {save_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading video: {e}")

# Example usage
author_uniqueid = "user123"
video_id = "456789"
tiktok_api_key = "YOUR_TIKTOK_API_KEY"  # Replace with your TikTok API key

downloader = TikTokDownloader(author_uniqueid, video_id, tiktok_api_key)
downloader.download_video("video.mp4")  # Save the video as "video.mp4"
