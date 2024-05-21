from PIL import Image
from io import BytesIO
import requests;

def download_image(image_url: str, file_path: str):
    """
    指定されたURLから画像をダウンロードし、指定されたファイルパスに保存する。
    """
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.save(file_path)