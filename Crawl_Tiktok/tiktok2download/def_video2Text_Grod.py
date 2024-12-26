from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
import os

# Get path to .env file
current_file = Path(__file__)
env_path = current_file.parent.parent / ".env"

# Debug: Read and print .env file content
print("\n=== .env file content ===")
try:
    with open(env_path, 'r', encoding='utf-8') as f:
        print(f.read())
except Exception as e:
    print(f"Error reading .env: {e}")

# Load environment variables
load_dotenv(dotenv_path=env_path)

# Get and clean API key
groq_key = os.getenv('GROQ_API_KEY', '').strip()
print("\n=== Environment Variable ===")
print(f"Raw API key value: '{groq_key}'")
print(f"API key length: {len(groq_key) if groq_key else 0}")

# Initialize Groq client with cleaned API key
client = Groq(
    api_key=groq_key
)

# Get current file's directory and construct path to video
video_path = current_file.parent / "video_downloaded" / "video_test.mp4"

# Add debug prints
print(f"Current file path: {current_file}")
print(f"Video path: {video_path}")
print(f"Video file exists: {video_path.exists()}")

# Check if file exists before opening
if not video_path.exists():
    raise FileNotFoundError(f"Video file not found at: {video_path}")

with open(video_path, "rb") as file:
    transcription = client.audio.transcriptions.create(
      file=(str(video_path), file.read()),
      model="whisper-large-v3",
      response_format="verbose_json",
    )
    print(transcription.text)
      