import requests

def text_to_speech(input_text=None, file_path=None, voice="en-AU-NatashaNeural", speed=1, output_file="2_1.mp3"):
    url = "http://103.253.20.13:25010/api/text-to-speech"
    headers = {"Content-Type": "application/json"}
    
    if input_text:
        text = input_text
    elif file_path:
        with open(file_path, "r") as file:
            text = file.read()
    else:
        raise ValueError("Either input_text or file_path must be provided.")
    
    data = {"text": text, "voice": voice, "speed": speed}
    response = requests.post(url, headers=headers, json=data)
    with open(output_file, "wb") as file:
        file.write(response.content)
    print(f"Audio file saved as {output_file}")

# Interview questions
text_to_speech("Tell me about yourself.", voice="en-AU-NatashaNeural", output_file="interview_1.mp3")

text_to_speech("Why are you interested in this position?", voice="en-AU-NatashaNeural", output_file="interview_2.mp3")

text_to_speech("What are your strengths?", voice="en-AU-NatashaNeural", output_file="interview_3.mp3")

text_to_speech("Where do you see yourself in five years?", voice="en-AU-NatashaNeural", output_file="interview_4.mp3")

text_to_speech("Do you have any questions for us?", voice="en-AU-NatashaNeural", output_file="interview_5.mp3")
