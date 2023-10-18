from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

token = "EAAM5aIf44WoBOzUKLoz7YeFJt1tV04YZBbGb7tZBZB76szXdgX6ltTVV7xosgZAWmI7kjWlQu5HZBs6ASZBl3CBJIDxce9helJHDI8P0eZCjFbvyfO5FknXZBjjhlzP0cDRTXi3AEuQvXck0hVCFJftt4oKZBc5xLNZBJZAEehZApTNJVZAmVCrNVPX4kZBI2AN1mOqXVjqUCDfYis82kcbTGmvXlFKwqWfPNqBGuEjrQ17e3eSH4ZD"
mytoken = "dockare"


@app.route('/')
def home():
    return "Hello, this is the webhook setup"


@app.route('/webhooks', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        challenge = request.args.get('hub.challenge')
        verify_token = request.args.get('hub.verify_token')

        if mode and verify_token:
            if mode == "subscribe" and verify_token == mytoken:
                return challenge, 200
            else:
                return "Verification failed", 403

    if request.method == 'POST':
        data = request.json
        print(data)

        if 'object' in data:
            # new code
            entry = data[0]['entry'][0]
            changes = entry['changes'][0]
            from_id = changes['value']['from']['id']
            # from_name = changes['value']['from']['name']
            # post_type = changes['value']['post']
            message = changes['value']['message']

            phone_number_id = 150495521475501
            recipient_id = from_id
            message_body = message

            print(f"Phone number: {phone_number_id}")
            print(f"From: {recipient_id}")
            print(f"Message Body: {message_body}")

            response_data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "text": {
                    "body": "hii from dockare"
                }
            }

            response = requests.post(f"https://graph.facebook.com/v17.0/{phone_number_id}/messages",
                                     json=response_data, headers={"Authorization": f"Bearer {token}",
                                                                  "Content-Type": "application/json"})

            if response.status_code == 200:
                return "OK", 200
            else:
                return "Failed to send message", 500

    return "Not Found", 404


if __name__ == '__main__':
    app.run()

