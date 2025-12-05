# tests/test_pose.py
import sys
import os

# Add project root directory to sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

print("ROOT_DIR:", ROOT_DIR)
print("sys.path:", sys.path[:5])  # Debug

import os
from pose_analyzer import analyze_video
import cv2
import numpy as np

def make_dummy_video(path="tests/data/dummy.mp4", frames=5, w=320, h=240):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(path, fourcc, 15, (w,h))
    for i in range(frames):
        img = (np.random.rand(h,w,3)*255).astype('uint8')
        out.write(img)
    out.release()
    return path

def test_analyze_video_creates_output(tmp_path):
    in_video = make_dummy_video("tests/data/dummy.mp4")
    out_video = str(tmp_path / "out.mp4")
    frames, width, fps = analyze_video(in_video, out_video, max_frames=3)
    assert frames > 0
    cap = cv2.VideoCapture(out_video)
    assert cap.isOpened()
    out_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    assert out_frames > 0
    cap.release()
