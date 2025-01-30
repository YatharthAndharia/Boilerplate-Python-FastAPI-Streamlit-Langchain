import streamlit as st
import requests
import os
import json
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path(__file__).resolve().parent.parent.parent / "streamlit.env"
load_dotenv(dotenv_path)

# API URL (replace with your actual API endpoint)
API_URL = os.getenv('API_BASE_URL')+'/add-account'

def main():
    st.set_page_config(
        page_title="Add New Account",
        page_icon="🆕",
        layout="wide",
    )
    st.title("Accounts Data Entry")

    # Form for data entry
    with st.form("data_entry_form"):
        account_name = st.text_input("**Account Name**", max_chars=255, help="Enter the name of the account.")
        account_number = st.text_input("**Account Number** (optional)", max_chars=50, help="Enter the unique account number.")
        balance = st.number_input("**Balance**", min_value=0.0, step=0.01, format="%.2f", help="Enter the initial balance for the account.")

        # Submit button
        submitted = st.form_submit_button("Submit")

    # Handle form submission
    if submitted:
        # Validate form fields
        if not account_name:
            st.error("Account Name is required.")
        else:
            # Prepare data payload
            payload = {
                "account_name": account_name,
                "account_number": account_number,
                "balance": balance
            }

            try:
                # Send data to the API
                response = requests.post(API_URL, json=payload)

                # Check API response
                if response.status_code == 201:
                    st.success("Account successfully added to the database!")
                elif response.status_code == 400:
                    st.error(f"Bad Request: {json.loads(response.content)}")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
