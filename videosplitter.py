import cv2
import os
from moviepy.editor import VideoFileClip
from pydub import AudioSegment

def extract_frames_and_audio(video_path, frames_dir, audio_snippets_dir, interval=1):
    '''
    Extracts frames and audio snippets from a video at specified intervals.
    '''
    # Create directories if they don't exist
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(audio_snippets_dir, exist_ok=True)
    
    # Extract frames
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open the video file: Check the path or file format.")
    
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(frame_rate * interval)
    frame_id = 0
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        if frame_id % frame_interval == 0:
            timestamp = frame_id / frame_rate
            timestamp_formatted = f'{timestamp:.2f}'
            frame_filename = os.path.join(frames_dir, f'timestamp_{timestamp_formatted}.jpg')
            if frame is not None and not frame.size == 0:
                cv2.imwrite(frame_filename, frame)
        frame_id += 1
    
    cap.release()
    
    # Extract audio snippets
    video = VideoFileClip(video_path)
    audio = video.audio
    duration = int(video.duration)
    
    for t in range(0, duration, interval):
        snippet = audio.subclip(t, min(t + interval, duration))
        snippet_path = os.path.join(audio_snippets_dir, f'snippet_{t}.wav')
        snippet.write_audiofile(snippet_path)

try:
    extract_frames_and_audio("SmallTalk.mp4", "my_frames", "my_audio_snippets", interval=1)
except ValueError as e:
    print(e)
