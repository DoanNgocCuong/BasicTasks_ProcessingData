import pandas as pd
import requests
from moviepy.editor import AudioFileClip, concatenate_audioclips
import os

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(SCRIPT_DIR, "temp")

# Create temp directory if it doesn't exist
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

def text_to_speech(input_text=None, file_path=None, voice="en-AU-NatashaNeural", speed=1, output_file="output.mp3"):
    """Generate speech from text using the TTS API"""
    url = "http://103.253.20.13:25010/api/text-to-speech"
    headers = {"Content-Type": "application/json"}
    output_path = os.path.join(TEMP_DIR, output_file)
    
    # Handle text input from file or direct text
    if input_text:
        text = input_text
    elif file_path:
        with open(file_path, "r") as file:
            text = file.read()
    else:
        raise ValueError("Either input_text or file_path must be provided.")
    
    data = {"text": text, "voice": voice, "speed": speed}
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        with open(output_path, "wb") as file:
            file.write(response.content)
        print(f"Created: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error creating {output_file}: {str(e)}")
        return None

def process_excel_to_audio(excel_file, sheet_name="Sheet1"):
    """Process each row in Excel file to create audio files"""
    try:
        # Read Excel file
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        created_files = []
        
        # Validate required columns
        required_columns = ['text', 'voice', 'output_file']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Process each row
        for index, row in df.iterrows():
            # Get parameters with defaults
            text = row['text']
            voice = row['voice']
            output_file = row['output_file']
            speed = row.get('speed', 1)
            file_path = row.get('file_path', None)
            
            # Create audio file
            audio_file = text_to_speech(
                input_text=text if pd.notna(text) else None,
                file_path=file_path if pd.notna(file_path) else None,
                voice=voice,
                speed=speed,
                output_file=output_file
            )
            
            if audio_file:
                created_files.append(audio_file)
        
        return created_files
    
    except Exception as e:
        print(f"Error processing Excel file: {str(e)}")
        return []

def merge_audio_files(input_files, output_file="final_output.mp3"):
    """Merge all audio files into one"""
    audio_clips = []
    output_path = os.path.join(SCRIPT_DIR, output_file)
    
    try:
        # Read each audio file
        for file in input_files:
            # Check if the file is in temp directory or script directory
            temp_path = os.path.join(TEMP_DIR, file)
            script_path = os.path.join(SCRIPT_DIR, file)
            
            if os.path.exists(temp_path):
                file_path = temp_path
            elif os.path.exists(script_path):
                file_path = script_path
            else:
                print(f"Warning: File {file} not found")
                continue
                
            clip = AudioFileClip(file_path)
            audio_clips.append(clip)
        
        if audio_clips:
            # Merge clips
            final_clip = concatenate_audioclips(audio_clips)
            
            # Save file
            final_clip.write_audiofile(output_path)
            
            # Close clips
            for clip in audio_clips:
                clip.close()
            final_clip.close()
            
            print(f"Successfully created {output_file}!")
            
            # Clean up temp files (only files in temp directory)
            for file in input_files:
                temp_path = os.path.join(TEMP_DIR, file)
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    print(f"Deleted temp file: {file}")
            
            # Remove temp directory if empty
            if not os.listdir(TEMP_DIR):
                os.rmdir(TEMP_DIR)
                print("Removed empty temp directory")
                
            return True
            
    except Exception as e:
        print(f"Error merging audio files: {str(e)}")
        return False

if __name__ == "__main__":
    excel_file = "tts_script.xlsx"
    
    # List of additional audio files (like background music, transitions)
    additional_files = [
        "interview_sceneTransition.mp3",
        "silent_1sec.mp3",
        "silent_3sec.mp3"
    ]
    
    print("Starting audio generation...")
    created_files = process_excel_to_audio(excel_file)
    
    if created_files:
        # Combine created files with additional files in the correct order
        input_files = []
        scenario_count = 3  # Number of scenarios
        
        # Add intro
        intro_file = next((f for f in created_files if f.startswith('intro')), None)
        if intro_file:
            input_files.append(intro_file)
            
        # Add each scenario with transitions
        for i in range(1, scenario_count + 1):
            # Add transition
            input_files.append("interview_sceneTransition.mp3")
            
            # Add scenario files in order
            scenario_files = [f for f in created_files if f.startswith(f'scenario{i}')]
            for file in scenario_files:
                input_files.append(file)
                # Add pause after each scenario
                input_files.append("silent_3sec.mp3")
        
        print("\nMerging audio files...")
        success = merge_audio_files(input_files, "final_lesson.mp3")
        if success:
            print("\nProcess completed successfully!")
        else:
            print("\nError occurred during merging.")
    else:
        print("\nNo audio files were created.")