from fastapi import FastAPI, Request
from twilio.rest import Client
from dotenv import load_dotenv
import os

app = FastAPI()

# Light status
light_status = {"state": "off"}


load_dotenv()

# Configure Twilio
account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
whatsapp_number = os.getenv("WHATSAPP_NUMBER")
client = Client(account_sid, auth_token)

@app.get("/light-status")
def get_light_status():
    return light_status

@app.post("/whatsapp")
async def whatsapp_command(request: Request):
    global light_status
    data = await request.form()
    message = data.get("Body").lower()

    if "turn on light" in message:
        light_status["state"] = "on"
        response_msg = "✅ Light turned on"
    elif "turn off light" in message:
        light_status["state"] = "off"
        response_msg = "✅ Light turned off"
    else:
        response_msg = "❌ Command not recognized"

    # WhatsApp response
    client.messages.create(
        body=response_msg,
        from_=whatsapp_number,
        to="whatsapp:your_number"
    )

    return {"message": "Command received"}