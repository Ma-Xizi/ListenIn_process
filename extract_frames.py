import cv2
import os

def extract_frames(path_to_video, frames_directory, frame_interval=2):
    
    cap = cv2.VideoCapture(path_to_video)

    if not cap.isOpened():
        raise ValueError("Could not open the video file: Check the path or file format.")

    if not os.path.exists(frames_directory):
        os.makedirs(frames_directory)

    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_interval_in_frames = int(frame_rate * frame_interval)
    frame_id = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        if frame_id % frame_interval_in_frames == 0:
            timestamp = frame_id / frame_rate
            timestamp_formatted = f'{timestamp:.2f}'
            frame_filename = os.path.join(frames_directory, f'timestamp_{timestamp_formatted}.jpg')
            if frame is not None and not frame.size == 0:
                cv2.imwrite(frame_filename, frame)

        frame_id += 1

    cap.release()

# Example usage
if __name__ == "__main__":
    try:
        extract_frames("my_video.MOV", "my_frames", frame_interval=2)
    except ValueError as e:
        print(e)
