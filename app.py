# app.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import shutil, os, uuid
from pose_analyzer import analyze_video

app = FastAPI(title="Dance Movement Analyzer")
TMP_DIR = "/tmp/dance_analyzer"
os.makedirs(TMP_DIR, exist_ok=True)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
        raise HTTPException(status_code=400, detail="Unsupported video format")

    uid = str(uuid.uuid4())
    in_path = os.path.join(TMP_DIR, f"{uid}_in_{file.filename}")
    out_path = os.path.join(TMP_DIR, f"{uid}_out.mp4")

    with open(in_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        analyze_video(in_path, out_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return FileResponse(out_path, media_type='video/mp4', filename=os.path.basename(out_path))
