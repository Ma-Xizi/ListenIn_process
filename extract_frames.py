import cv2
import os

def extract_frames(path_to_video, frames_directory):
    '''
    Method takes in a path to a video and the name of the directory to be created containing each frame,
    creates the directory if it does not exist, and puts the frames extracted from the directory in the video.
    '''
    cap = cv2.VideoCapture(path_to_video)

    # Check if video capture has been initialized correctly
    if not cap.isOpened():
        raise ValueError("Could not open the video file: Check the path or file format.")

    # Create the directory if it doesn't exist
    if not os.path.exists(frames_directory):
        os.makedirs(frames_directory)
        
    # Get frame rate
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_id = 0

    while True:
        success, frame = cap.read()
        if not success:
            break  # No more frames to read

        # Calculate the timestamp (in seconds)
        timestamp = frame_id / frame_rate
        timestamp_formatted = f'{timestamp:.2f}'

        # Save each frame with the timestamp as its name
        frame_filename = os.path.join(frames_directory, f'timestamp_{timestamp_formatted}.jpg')
        if frame is not None and not frame.size == 0:
            cv2.imwrite(frame_filename, frame)
        frame_id += 1

    # Release resources
    cap.release()

try:
    extract_frames("my_video.MOV", "my_frames")
except ValueError as e:
    print(e)
