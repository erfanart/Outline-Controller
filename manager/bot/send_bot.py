import requests
# import sys

def send_to_telegram(message,ApiURL,ChatID):
    try:
        response = requests. post(ApiURL, json={'chat_id': ChatID, 'text': message})
        print(response.text)
        
    except Exception as e:
        print(e)