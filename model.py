from langchain_openai import ChatOpenAI
import base64
import os
from typing import List
from extract_frames import extract_frames
from gtts import gTTS


llm = ChatOpenAI(
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
<<<<<<< Updated upstream
    api_key="API-KEY",
=======
    api_key="sk-proj-jJoV4a8oML8LI3OXVtUhT3BlbkFJucvjuL4Fm0YtvLxhVV0m",  # if you prefer to pass api key in directly instaed of using env vars
>>>>>>> Stashed changes
)

print(llm.invoke("Good mo"))

def load_image(inputs: dict) -> dict:
    """Load image from file and encode it as base64."""
    image_path = inputs["image_path"]

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    image_base64 = encode_image(image_path)
    return {"image": image_base64}

from langchain.chains import TransformChain
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain import globals
from langchain_core.runnables import chain

load_image_chain = TransformChain(
    input_variables=["image_path"],
    output_variables=["image"],
    transform=load_image
)

# Set verbose
globals.set_debug(True)

@chain
<<<<<<< Updated upstream
def image_model(inputs: dict) -> str:
    model = ChatOpenAI(temperature=0.5, max_tokens=1024, model="gpt-4o", api_key="API-KEY")
    msg = model.invoke(
        [HumanMessage(
            content=[
                {"type": "text", "text": inputs["prompt"]},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{inputs['image']}"}},
            ])]
    )
    return msg.content if msg else ""
=======
def image_model(inputs: dict) -> str | list[str] | dict:
 """Invoke model with image and prompt."""
 model = ChatOpenAI(temperature=0.5, max_tokens=1024, model="gpt-4o",api_key="sk-proj-jJoV4a8oML8LI3OXVtUhT3BlbkFJucvjuL4Fm0YtvLxhVV0m")
 msg = model.invoke(
             [HumanMessage(
             content=[
             {"type": "text", "text": inputs["prompt"]},
             {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{inputs['image']}"}},
             ])]
             )
 return msg.content
>>>>>>> Stashed changes

def get_image_information(image_path: str) -> str:
    vision_prompt = "Describe the image you see"
    vision_chain = load_image_chain | image_model 
    response = vision_chain.invoke({'image_path': image_path, 'prompt': vision_prompt})
    return response

def generate_summary(descriptions: List[str]) -> str:
    llm = ChatOpenAI(temperature=0.5, max_tokens=1024, model="gpt-4o", api_key="API-KEY")
    combined_descriptions = " ".join(descriptions)
    summary_prompt = f"The following descriptions are for video frames, summarize into a coherent summary of the video:\n\n{combined_descriptions}"
    summary_message = llm.invoke(summary_prompt)
    return summary_message.content if summary_message else ""

<<<<<<< Updated upstream
def get_video_summary(video_path: str, frames_directory: str) -> str:
    extract_frames(video_path, frames_directory, frame_interval=2)
    frame_files = [os.path.join(frames_directory, f) for f in os.listdir(frames_directory) if f.endswith('.jpg')]
    descriptions = [get_image_information(frame) for frame in frame_files]
    return generate_summary(descriptions)

def generate_audio_from_text(text: str, audio_file_path: str):
    tts = gTTS(text=text, lang='en')
    tts.save(audio_file_path)

# Example usage
try:
    video_summary = get_video_summary("my_video.MOV", "my_frames")
    print(video_summary)

    # Generate audio from the summary
    audio_file_path = "summary_audio.mp3"
    generate_audio_from_text(video_summary, audio_file_path)

    # Add the generated audio back to the video
    # Replace this with your method to add audio to video (e.g., using MoviePy)
    # Example:
    # add_audio_to_video("my_video.MOV", audio_file_path, "video_with_audio.MOV")

except ValueError as e:
    print(e)
=======
get_image_information("/Users/mw/Documents/GitHub/SignSage/my_frames/timestamp_0.00.jpg")
>>>>>>> Stashed changes
