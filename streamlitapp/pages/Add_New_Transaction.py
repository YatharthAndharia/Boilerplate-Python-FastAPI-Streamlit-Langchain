import streamlit as st
import requests
import datetime
import os
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path(__file__).resolve().parent.parent.parent / "streamlit.env"

load_dotenv(dotenv_path)

# API URLs (replace with your actual API endpoints)
GET_ACCOUNTS_API_URL = os.getenv('API_BASE_URL') + '/get-accounts'
ADD_TRANSACTION_API_URL = os.getenv('API_BASE_URL') + '/add-transaction'

def main():
    st.title("Add New Transaction")

    # Fetch accounts for dropdowns
    try:
        response = requests.get(GET_ACCOUNTS_API_URL)
        if response.status_code == 200:
            accounts_data = response.json()  # Assuming API returns a JSON array of accounts
            account_options = {account["account_name"]: account["id"] for account in accounts_data}
        else:
            st.error(f"Failed to fetch accounts: {response.status_code}")
            return
    except Exception as e:
        st.error(f"An error occurred while fetching accounts: {e}")
        return

    # Form for adding a transaction
    with st.form("add_transaction_form"):
        from_account = st.selectbox(
            "From Account",
            options=list(account_options.keys()),
            help="Select the account from which the funds will be transferred.",
        )
        to_account = st.selectbox(
            "To Account",
            options=list(account_options.keys()),
            help="Select the account to which the funds will be transferred.",
        )
        transaction_amount = st.number_input(
            "Transaction Amount",
            min_value=0.00,
            step=0.01,
            format="%.2f",
            help="Enter the amount for the transaction.",
        )
        transaction_date = st.date_input(
            "Transaction Date",
            value=datetime.date.today(),
            max_value=datetime.date.today(),
            help="Select the date of the transaction.",
        )
        remarks=st.text_input(
            "Remarks",
            help="Enter remarks for the transaction if any"
        )

        # Submit button
        submitted = st.form_submit_button("Submit Transaction")

    # Handle form submission
    if submitted:
        # Ensure From Account and To Account are different
        if from_account == to_account:
            st.error("From Account and To Account cannot be the same.")
        else:
            # Prepare data payload
            payload = {
                "from_account": account_options[from_account],
                "to_account": account_options[to_account],
                "transaction_amount": transaction_amount,
                "transaction_date": str(transaction_date),
                "remarks": remarks
            }

            # Send data to the API
            try:
                response = requests.post(ADD_TRANSACTION_API_URL, json=payload)

                # Handle API response
                if response.status_code == 201:
                    st.success("Transaction successfully recorded!")
                elif response.status_code == 400:
                    st.error(f"Bad Request: {response.content}")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
