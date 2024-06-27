import streamlit as st
import os
from extract_frames import extract_frames
from model import get_video_summary
from gtts import gTTS

# Function to ensure directory exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to convert text to audio using gTTS
def text_to_audio(text, audio_filename):
    tts = gTTS(text=text, lang='en')
    ensure_directory_exists(os.path.dirname(audio_filename))  # Ensure directory exists
    tts.save(audio_filename)

# Set up Streamlit
st.title("Video Summary Generator")
st.write("Upload a video file and get a summary of its content.")

# File uploader
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])

# Directory to save frames and audio
frames_directory = "uploaded_frames"
audio_directory = "uploaded_audio"

if uploaded_file is not None:
    # Save the uploaded video to a temporary file
    temp_video_path = os.path.join("temp", uploaded_file.name)
    
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.write(f"Uploaded {uploaded_file.name}")

    # Extract frames and generate summary
    try:
        with st.spinner("Extracting frames and generating summary..."):
            video_summary = get_video_summary(temp_video_path, frames_directory)
        st.success("Summary generated!")
        st.write(video_summary)

        # Generate audio from summary
        audio_filename = os.path.join(audio_directory, "summary_audio.mp3")
        text_to_audio(video_summary, audio_filename)

        # Display audio with a text caption
        st.write("Summary Audio")
        st.audio(audio_filename, format='audio/mp3')

    except ValueError as e:
        st.error(f"An error occurred: {e}")

    # Clean up temporary files
    if os.path.exists(temp_video_path):
        os.remove(temp_video_path)
    for file in os.listdir(frames_directory):
        os.remove(os.path.join(frames_directory, file))
    if os.path.exists(audio_filename):
        os.remove(audio_filename)

else:
    st.write("Please upload a video file.")
