from flask import Flask, request, jsonify
import requests
import os
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

app = Flask(__name__)
@app.route("/", methods=["GET"])
def home():
  return jsonify({"status": "ok"})

@app.route("/webhook", methods=["POST"])
def webhook():
  data = request.get_json()
  events = data.get("events", [])
  if events:
    event = events[0]
    reply_token = event.get("replyToken")
    message = event.get("message", {})
    text = message.get("text", "")
    if reply_token and text:
      headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
        }
      body = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": f"受信しました：{text}"}]
        }
      requests.post(
        "https://api.line.me/v2/bot/message/reply",
        headers=headers,
        json=body
        )
  return jsonify({"received": True})

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080)
