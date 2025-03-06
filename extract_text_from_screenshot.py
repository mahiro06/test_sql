import os
import time
from google.cloud import vision
from google.cloud.vision_v1 import types
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load environment variables from .env file
load_dotenv('/Users/nakajimahirotaka/VScode/test_sql/.env')

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
    
    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
    lines = text.split('\n')
    for line in lines:
        if line.strip():  # 空行を無視
            if '¥' in line:
                text_part, amount_part = line.split('¥', 1)
                sheet.append_row([text_part.strip(), '¥' + amount_part.strip()])
            else:
                sheet.append_row([line.strip()])
            time.sleep(0.1)  # 0.1秒の待機を追加してリクエスト頻度を制限

if __name__ == "__main__":
    image_path = '/Users/nakajimahirotaka/Pictures/test_date.png'
    sheet_id = os.getenv('SHEET_ID')
    sheet_name = os.getenv('SHEET_NAME')
    
    text = extract_text_from_image(image_path)
    update_spreadsheet(sheet_id, sheet_name, text)
