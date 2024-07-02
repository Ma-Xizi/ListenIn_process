from langchain_openai import ChatOpenAI
from langchain.chains import TransformChain
from langchain_core.runnables import chain
from langchain_core.messages import HumanMessage

import base64
import speech_recognition as sr
import os

# Initialize OpenAI ChatOpenAI instance
llm = ChatOpenAI(
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key="apikey"  # Replace with your API key
)

# Function to load image and encode as base64
def load_image(inputs: dict) -> dict:
    image_path = inputs["image_path"]
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    return {"image": image_base64}

# Setup chain to load image and invoke model

load_image_chain = TransformChain(
    input_variables=["image_path"],
    output_variables=["image"],
    transform=load_image
)

# Set verbose
from langchain import globals
globals.set_debug(True)

# Define chain for image model invocation
@chain
def image_model(inputs: dict) -> str | list[str] | dict:
    model = ChatOpenAI(temperature=0.5, max_tokens=1024, model="gpt-4o", api_key="apikey")
    msg = model.invoke(
        [HumanMessage(
            content=[
                {"type": "text", "text": inputs["prompt"]},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{inputs['image']}"}},
            ]
        )]
    )
    return msg.content

# Function to get image information and description
def get_image_information(image_path: str) -> str:
    vision_prompt = """
    Describe the image you see
    """
    vision_chain = load_image_chain | image_model
    result = vision_chain.invoke({'image_path': image_path, 'prompt': vision_prompt})
    return result

# Function to transcribe audio to text using speech recognition
def transcribe_audio(audio_path: str) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

# Example usage with one image and one audio snippet
def process_single_image_and_audio(image_path: str, audio_path: str) -> str:
    # Get scene description from the image
    scene_description = get_image_information(image_path)
    
    # Transcribe audio snippet
    audio_transcription = transcribe_audio(audio_path)
    
    # Combine scene description with audio transcription
    combined_text = f"Scene Description: {scene_description}\nAudio Transcription: {audio_transcription}"
    
    return combined_text

# Example usage:
image_path = "/Users/mw/Documents/GitHub/SignSage/my_frames/timestamp_0.96.jpg"
audio_path = "/Users/mw/Documents/GitHub/SignSage/my_audio_snippets/snippet_1.wav"

combined_text = process_single_image_and_audio(image_path, audio_path)
print(combined_text)
