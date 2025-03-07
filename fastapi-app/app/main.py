import os
import cv2

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

app = FastAPI()

def generate_frames():

    load_dotenv()

    username = os.getenv("CAMERA_USERNAME")
    password = os.getenv("CAMERA_PASSWORD")
    ip_address = os.getenv("CAMERA_IP")
    port = os.getenv("CAMERA_PORT")
    stream = os.getenv("CAMERA_STREAM")

    camera_url = f"rtsp://{username}:{password}@{ip_address}:{port}/{stream}"
    cap = cv2.VideoCapture(camera_url)

    while True:
        success, frame = cap.read()
        if not success:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
