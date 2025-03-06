import os
import time
from google.cloud import vision
from google.cloud.vision_v1 import types
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Set the environment variable for Google Cloud Vision API credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('CREDENTIALS_JSON')

def extract_text_from_image(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description
    return ""

def update_spreadsheet(sheet_id, sheet_name, text):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials_path = os.getenv('CREDENTIALS_JSON')
    if not credentials_path or not os.path.exists(credentials_path):
        raise FileNotFoundError("The credentials JSON file path is not set or the file does not exist.")
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
    
    lines = text.split('\n')
    rows = [[line.strip()] for line in lines if line.strip()]  # 空行を無視
    print(f"Appending rows: {rows}")  # デバッグ用のログ出力

    # 一行ごとに書き込む
    for row in rows:
        sheet.append_row(row)

if __name__ == "__main__":
    image_path = '/Users/nakajimahirotaka/Pictures/test_date.png'
    sheet_id = os.getenv('SHEET_ID')
    sheet_name = os.getenv('SHEET_NAME')
    
    text = extract_text_from_image(image_path)
    print(f"Extracted text: {text}")  # デバッグ用のログ出力
    update_spreadsheet(sheet_id, sheet_name, text)
