from moviepy.editor import AudioFileClip, concatenate_audioclips
import os

def merge_audio_files(input_files, output_file):
    # Tạo list các audio clips
    audio_clips = []
    
    try:
        # Đọc từng file audio
        for file in input_files:
            # Tách tên file gốc (không có đuôi)
            base_name = file.rsplit('.', 1)[0] if '.' in file else file
            
            # Kiểm tra cả hai phiên bản của file
            if os.path.exists(base_name + '.mp3'):
                actual_file = base_name + '.mp3'
            elif os.path.exists(base_name + '.wav'):
                actual_file = base_name + '.wav'
            else:
                print(f"Lỗi: Không tìm thấy file {base_name} với đuôi .mp3 hoặc .wav")
                return
                
            clip = AudioFileClip(actual_file)
            audio_clips.append(clip)
        
        # Ghép các clips
        final_clip = concatenate_audioclips(audio_clips)
        
        # Lưu file
        final_clip.write_audiofile(output_file)
        
        # Đóng các clips để giải phóng bộ nhớ
        for clip in audio_clips:
            clip.close()
        final_clip.close()
        
        print(f"Đã tạo file {output_file} thành công!")
        
    except Exception as e:  
        print(f"Lỗi: {str(e)}")

# Sử dụng hàm
input_files = ["idea3_1_1.wav", "interview_background_5sec.mp3",
               "idea3_1_2.wav", "CungTraLoiThuXem.wav", "interview_background_5sec.mp3",
               "idea3_1_3.wav", "CungTraLoiThuXem.wav", "interview_background_5sec.mp3",
               "idea3_1_4.wav", "CungTraLoiThuXem.wav", "interview_background_5sec.mp3",
               "idea3_1_5.wav",
               "idea3_1_6.wav",
               "idea3_1_7.wav"]
output_file = "idea3_final.mp3"

merge_audio_files(input_files, output_file)