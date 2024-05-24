from fastapi.testclient import TestClient
from main import app
import io

client = TestClient(app)

def test_create_upload_file():
    # テスト用の画像ファイルを作成
    file_content = b'a' * 1024  # 1KBのダミーデータ
    data = {'file': ('test.jpg', io.BytesIO(file_content), 'image/jpeg')}
    
    # アップロードエンドポイントをテスト
    response = client.post("/upload/", files=data)
    
    # ステータスコードとレスポンスの内容を検証
    assert response.status_code == 200
    assert 'processed_test.jpg' in response.json()['filename']

def test_invalid_image_format():
    # 不正な画像フォーマットのテスト
    file_content = b'invalid_image_data'
    data = {'file': ('test.jpg', io.BytesIO(file_content), 'image/jpeg')}
    
    # アップロードエンドポイントをテスト
    response = client.post("/upload/", files=data)
    
    # ステータスコードとエラーメッセージを検証
    assert response.status_code == 400
    assert response.json()['detail'] == "Invalid image format"

# def test_no_faces_detected():
#     # 顔が検出されない画像のテスト
#     # ここでは適切な画像データを用意する必要があります。
#     # この例では、顔が含まれていない画像ファイルを想定しています。
#     file_content = b'...'  # 顔が含まれていない画像データ
#     data = {'file': ('noface.jpg', io.BytesIO(file_content), 'image/jpeg')}
    
#     # アップロードエンドポイントをテスト
#     response = client.post("/upload/", files=data)
    
#     # ステータスコードとエラーメッセージを検証
#     assert response.status_code == 400
#     assert response.json()['detail'] == "No faces detected"