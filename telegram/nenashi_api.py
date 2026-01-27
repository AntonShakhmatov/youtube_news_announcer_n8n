import requests
import os

GET_NENASHI_TOKEN = os.getenv('GET_NENASHI_TOKEN')

chat_id = -1003436296630

url = f"https://api.telegram.org/bot{GET_NENASHI_TOKEN}/getUpdates"

resp = requests.get(url)
data = resp.json()

if not data["ok"]:
    print("error", data)
    exit()

for update in data["result"]:
    if "channel_post" in update:
        post = update["channel_post"]

        if post["chat"]["id"] == chat_id:
            text = post.get("text")
            data = post.get("date")
            msg_id = post.get("message_id")

            print(f"[{msg_id}] {text}")