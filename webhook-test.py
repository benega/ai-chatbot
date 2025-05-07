import os
from flask import Flask, request

app = Flask(__name__)

WHATSAPP_API_TOKEN = os.environ.get("WHATSAPP_API_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_VERIFY_TOKEN = os.environ.get("WHATSAPP_VERIFY_TOKEN")

@app.route('/webhook', methods=['POST'])
def webhook():
    print('Webhook received!')
    print(request.json)
    print(WHATSAPP_API_TOKEN)
    print(WHATSAPP_PHONE_NUMBER_ID)
    print(WHATSAPP_VERIFY_TOKEN)
    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
