import os
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account

def transcribe_audio(audio_file_path, language_code="en-US"):
    # Set path to your Google Cloud credentials JSON file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/mw/Documents/GitHub/SignSage/cloud.json"  # Replace with your actual path

    # Initialize the Speech-to-Text client
    client = speech.SpeechClient()

    # Configure the audio file
    audio = {"uri": f"gs://{audio_file_path}"}

    config = {
        "language_code": language_code,
    }

    # Perform the transcription
    response = client.long_running_recognize(
        request={
            "config": config,
            "audio": audio
        }
    )

    # Wait for the transcription to complete
    operation = response.operation
    response = operation.result()

    # Extract the transcript
    transcript = ""
    for result in response.results:
        for alternative in result.alternatives:
            transcript += alternative.transcript + "\n"

    return transcript.strip()

# Example usage
audio_file_path = "/Users/mw/Documents/GitHub/SignSage/my_audio_snippets/snippet_1.wav"  # Replace with your actual audio file path in Google Cloud Storage
transcript = transcribe_audio(audio_file_path)
print(f"Transcript:\n{transcript}")
