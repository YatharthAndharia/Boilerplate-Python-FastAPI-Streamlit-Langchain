import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path(__file__).resolve().parent.parent.parent / "streamlit.env"

load_dotenv(dotenv_path)

# Streamlit UI
st.set_page_config(page_title="AI-Bot", page_icon='🧠',layout="wide")

# Title and description
st.title("🧠 AI-Bot")

# Input box for the question
question = st.text_input("**Enter your question:**", placeholder="E.g., Show all transactions with amounts greater than 1000")
api_url=os.getenv('API_BASE_URL') + '/ai-bot'
# Button to trigger API call
if st.button("Submit"):
    if question.strip():
        try:
            # Send the question to the API
            payload = {"question": question}
            response = requests.post(api_url, json=payload)

            # Handle the API response
            if response.status_code == 200:
                data = response.json()    
                st.write(json.loads(data)["ai_answer"])
            else:
                st.error(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a question before submitting.")
