import os, sys
from flask import Flask, request
from pymessenger import Bot
from utils import wit_response

VERIFY_TOKEN = "botchat"

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAEgZC2rkEq0BAItrPL2v4pN5PIoXUZBDgLSqsCr2KLsYV4vxb5b18kv3f8sY36dFTnmbWd1doUvkynUqMhxP7aUHtmbuTHlx1viNqwNXIaHbW0MD2rzXJsr78ZBg4xNHggiXrhZCvO3SVKvAZADSCZC3St4eEnn9u2VkM4NZCNogZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route("/", methods=["GET"])

def verify_token():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismach", 403
        return request.args["hub.challenge"], 200
    return "Hello World", 200


@app.route("/", methods=["POST"])

def webhook():
    data = request.get_json()
    log(data)
    
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                
                #ID
                sender_id = messaging_event["sender"]["id"]
                recipient_id = messaging_event["recipient"]["id"]
                
                if messaging_event.get("message"):
                    #extract message
                    if "text" in messaging_event["message"]:
                        messaging_text = messaging_event["message"]["text"]
                    else:
                        messaging_text = "no text"
                
                    #echo
                    response = None
                    entity, value = wit_response(messaging_text)
                    
                    if entity == "quadros":
                        response = "Nossos modelos são esses:"
                        
                    if response == None:
                        response = "Desculpe, não entendi :/"
                    bot.send_text_message(sender_id, response)
    
    return "ok", 200

def log(message):
    print (message)
    sys.stdout.flush()
    
    
if __name__ == "__main__":
    app.run(debug=False, port=80)
