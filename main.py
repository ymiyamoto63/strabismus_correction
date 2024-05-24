from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import cv2
import numpy as np

app = FastAPI()

origins = [
    "http://localhost:8080",  # Vue.jsが実行されているポート
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    upload_dir = "uploads"
    file_location = f"{upload_dir}/{file.filename}"
    # uploadsディレクトリが存在しない場合は作成
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    with open(file_location, "wb+") as file_object:
        file_data = await file.read()
        file_object.write(file_data)
    
    # 画像ファイルを読み込む
    image = cv2.imdecode(np.frombuffer(file_data, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image format")

    # 顔検出のための準備
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # 顔が検出されなかった場合
    if len(faces) == 0:
        raise HTTPException(status_code=400, detail="No faces detected")

    # 顔が検出された場合の処理（具体的な処理はここに記述）
    # 例: 検出された顔の領域を画像に矩形で描画
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # 処理後の画像を保存
    processed_file_location = f"{upload_dir}/processed_{file.filename}"
    cv2.imwrite(processed_file_location, image)

    content = {"filename": processed_file_location}
    return JSONResponse(status_code=200, content=content)
