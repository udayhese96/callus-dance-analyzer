# pose_analyzer.py
import cv2
import mediapipe as mp
from typing import Tuple

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def analyze_video(input_path: str, output_path: str, max_frames: int = None, draw_landmarks: bool = True) -> Tuple[int, int, float]:
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open {input_path}")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    with mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False) as pose:
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_idx += 1
            if max_frames and frame_idx > max_frames:
                break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)
            if draw_landmarks and results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0,128,255), thickness=2))
            out.write(frame)
    cap.release()
    out.release()
    return frame_idx, width, fps

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python pose_analyzer.py input.mp4 output.mp4")
    else:
        analyze_video(sys.argv[1], sys.argv[2])
