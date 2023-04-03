from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/whatsappwebhook', methods=['GET'])
def whatsapp_webhook():
    # You can access query parameters using request.args.get()
    # For example, if your webhook has a query parameter 'message':
    # message = request.args.get('message', '')

    response = {
        "status": "success",
        "message": "WhatsApp webhook received"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
