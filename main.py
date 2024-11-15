import requests
import json
import gradio as gr
from datetime import datetime
import os

# Function to get time-based greeting
def get_time_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"

# Function to get response from Copilot API
def get_copilot_response(user_input):
    url = "https://copilot5.p.rapidapi.com/copilot"
    payload = {
        "message": f"{get_time_greeting()}! {user_input}",
        "conversation_id": None,  # New conversation each time
        "tone": "BALANCED",
        "markdown": False,
        "photo_url": None
    }
    headers = {
        "x-rapidapi-key": "205ec5f0cbmsh14b0a5092ae9041p11c95fjsn5b262371c67e",
        "x-rapidapi-host": "copilot5.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        # Sending the request to Copilot API
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        # Debugging print statement
        print("API Response:", data)

        # Check if the response contains the 'data' key with a 'message'
        if 'data' in data and 'message' in data['data']:
            return data['data']['message']
        else:
            return "Sorry, I couldn't get a valid message from the API. Please try again later."
    except Exception as e:
        return f"Error occurred: {str(e)}"

# Chatbot function that integrates greeting with Copilot API response
def chatbot(user_input):
    greeting = get_time_greeting()
    response = get_copilot_response(user_input)
    return f"{greeting}!\n\n{response}"

# Gradio interface setup
interface = gr.Interface(
    fn=chatbot,
    inputs="text",
    outputs="text",
    title="AgricChatBot",
    description="Welcome to **AgricChatBot**, your trusted assistant for agriculture inquiries, specializing in crops. Created by Group Two **Joseph, Wamunyima, and Obed**, we provide expert advice on **planting, pest control, and harvesting**. Ask us your questions — we’re here to support your farming success!!",
    css="style.css"
)

# Launch the Gradio app
if __name__ == "__main__":
    interface.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8000)))

