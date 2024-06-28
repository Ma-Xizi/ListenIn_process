from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
import os
import cv2

def save_scenes(video_path, scenes, output_folder):
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for i, scene in enumerate(scenes):
        start_frame, end_frame = scene
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        ret, frame = cap.read()
        if ret:
            timestamp = start_frame / frame_rate
            timestamp_formatted = f'{timestamp:.2f}'
            frame_filename = os.path.join(output_folder, f'scene_{i}_timestamp_{timestamp_formatted}.jpg')
            cv2.imwrite(frame_filename, frame)
    
    cap.release()

def detect_scenes(video_path, output_folder):
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=20.0))

    video_manager.set_downscale_factor()
    video_manager.start()
    
    scene_manager.detect_scenes(frame_source=video_manager)
    scene_list = scene_manager.get_scene_list()
    
    scene_frame_numbers = [(scene[0].get_frames(), scene[1].get_frames()) for scene in scene_list]
    
    save_scenes(video_path, scene_frame_numbers, output_folder)
    
    video_manager.release()

# Example usage
video_path = 'my_video.MOV'
output_folder = 'my_scenes'

detect_scenes(video_path, output_folder)
