import os
import time
from dotenv import load_dotenv
import pytesseract
from PIL import Image
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv('/Users/nakajimahirotaka/VScode/test_sql/.env')

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='jpn')
    return text

def update_spreadsheet(sheet_id, sheet_name, text):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials_path = os.getenv('CREDENTIALS_JSON')
    if not credentials_path or not os.path.exists(credentials_path):
        raise FileNotFoundError("The credentials JSON file path is not set or the file does not exist.")
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    
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
