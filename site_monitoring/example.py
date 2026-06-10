import requests

# Sozlamalar
URL = "https://api.otaboyev-prep.uz/api/files"
TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJnYW5pc2hlcm90YWJveWV2MUBnbWFpbC5jb20iLCJpYXQiOjE3ODAxNzI4MDQsImV4cCI6MTc4Nzk0ODgwNH0.fQQGvQCV0MEo0jKbcIumYg8ZGjahQsgMlZJxsoTJowD7OgfSgRuqw_-QniyO-cyAmEXg1510WB3zNaLTLyQNsQ"  # Login orqali olingan tokenni shu yerga qo'ying
FILE_PATH = "test.txt"       # Yuklamoqchi bo'lgan faylingiz manzili

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# Faylni ochish
files = {
    "file": open(FILE_PATH, "rb")
}

# Query parametrlar (description va category)
params = {
    "description": "Test fayl yuklash",
    "category": "document"
}

try:
    response = requests.post(URL, headers=headers, files=files, params=params)
    
    if response.status_code == 200:
        print("Muvaffaqiyatli yuklandi!")
        print("Javob:", response.json())
    else:
        print(f"Xatolik yuz berdi: {response.status_code}")
        print("Tafsilot:", response.text)
        
except Exception as e:
    print(f"So'rovda xatolik: {e}")