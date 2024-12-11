from credentials import TELEGRAM_CHAT_ID, TELEGRAM_AUTH_TOKEN
import requests

TEXT = "test method"
URL = "https://api.telegram.org/bot"+TELEGRAM_AUTH_TOKEN+"/sendMessage"

def sendMessage(message):
    try:
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(URL, json=data)
        if response.status_code == 200:
            print(message, "Sent telegram successfully!")
        else:
            print("Error sending telegram message:", response.text)
    except Exception as e:
        print(e)
        print(message, "Failed to send text")
        