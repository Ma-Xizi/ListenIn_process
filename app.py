import streamlit as st
import os
from gtts import gTTS
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
from model import get_video_summary, extract_audio_from_video, process_video_part  # Assuming model.py is in the same directory

# Function to convert text to audio using gTTS
def text_to_audio(text, audio_filename):
    tts = gTTS(text=text, lang='en')
    tts.save(audio_filename)

# Function to add audio to video using moviepy
def add_audio_to_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    video = video.set_audio(audio)
    video.write_videofile(output_path, codec='libx264', audio_codec='aac', threads=4)  # Utilize multiple threads for faster processing
    audio.close()
    video.close()

# Set up Streamlit
st.title("Video Summary Generator")
st.write("Upload a video file and get a summary of its content.")

# File uploader
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])

# Directory to save frames, audio, and output video
frames_directory = "uploaded_frames"
audio_directory = "uploaded_audio"
output_directory = "output_videos"

# Ensure directories exist
os.makedirs(frames_directory, exist_ok=True)
os.makedirs(audio_directory, exist_ok=True)
os.makedirs(output_directory, exist_ok=True)

if uploaded_file is not None:
    # Save the uploaded video to a temporary file
    temp_video_path = os.path.join("temp", uploaded_file.name)
    
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.write(f"Uploaded {uploaded_file.name}")

    try:
        with st.spinner("Extracting frames and generating summary..."):
            # Generate video summary
            video_summary = get_video_summary(temp_video_path, frames_directory)
        
        st.success("Summary generated!")
        st.write(video_summary)

        # Generate audio from summary
        audio_filename = os.path.join(audio_directory, "summary_audio.mp3")
        text_to_audio(video_summary, audio_filename)

        # Add audio to the original video
        output_video_path = os.path.join(output_directory, "video_with_summary.mp4")
        add_audio_to_video(temp_video_path, audio_filename, output_video_path)

        # Display video with summary audio
        st.video(output_video_path)

        # Clean up temporary files (optional)
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)

        for file in os.listdir(frames_directory):
            os.remove(os.path.join(frames_directory, file))
        
        if os.path.exists(audio_filename):
            os.remove(audio_filename)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.write("Please upload a video file.")
