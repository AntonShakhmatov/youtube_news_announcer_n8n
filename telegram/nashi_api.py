import requests
import os

GET_NASHI_TOKEN = os.getenv('GET_NASHI_TOKEN')

chat_id = -1003086290508

url = f"https://api.telegram.org/bot{GET_NASHI_TOKEN}/getUpdates"

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