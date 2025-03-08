from fastapi import FastAPI, Request
from dotenv import load_dotenv

import openai
import requests
import os

app = FastAPI()
load_dotenv()

# Home Assistant Configuration
HOME_ASSISTANT_URL = os.getenv("HOME_ASSISTANT_URL", "http://localhost:8123")
LONG_LIVED_ACCESS_TOKEN = os.getenv("LONG_LIVED_ACCESS_TOKEN", "your-token-here")

#TODO: find a better way to manage these identifiers
ENTITY_ID = os.getenv("ENTITY_ID", "switch.sonoff_light")

openai.api_key = os.getenv("OPENAI_API_KEY", "your-openai-api-key")

headers = {
    "Authorization": f"Bearer {LONG_LIVED_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Function to control the light through Home Assistant
def control_light(action: str):
    payload = {"state": "on" if action == "on" else "off"}
    response = requests.post(
        f"{HOME_ASSISTANT_URL}/api/states/{ENTITY_ID}",
        headers=headers,
        json=payload
    )
    return response.json()

# Function to process the message with AI
def interpret_message(message: str):
    prompt = f"You are a home automation assistant. Respond with 'turn on' or 'turn off' if the user wants to control the light. Message: {message}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=10
    )
    return response['choices'][0]['text'].strip().lower()

# Route to receive WhatsApp messages from Twilio
@app.post("/whatsapp")
async def receive_message(request: Request):
    data = await request.form()
    message = data.get("Body")

    action = interpret_message(message)

    if action == "turn on":
        control_light("on")
        response_msg = "✅ Light turned on"
    elif action == "turn off":
        control_light("off")
        response_msg = "🌑 Light turned off"
    else:
        response_msg = "❓ I didn't understand your command. Try saying 'turn on the light' or 'turn off the light'."

    return response_msg