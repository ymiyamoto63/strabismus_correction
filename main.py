from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

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
        file_object.write(await file.read())
    return JSONResponse(status_code=200, content={"filename": file.filename})
