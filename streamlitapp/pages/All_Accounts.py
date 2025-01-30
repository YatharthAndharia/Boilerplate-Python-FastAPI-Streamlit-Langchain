import streamlit as st
import pandas as pd
import requests
import os
import json
from dotenv import load_dotenv

from pathlib import Path
dotenv_path = Path(__file__).resolve().parent.parent.parent / "streamlit.env"

load_dotenv(dotenv_path)

# API URLs (replace with your actual API endpoints)
GET_ACCOUNTS_API_URL = os.getenv('API_BASE_URL') + '/get-accounts'
UPDATE_ACCOUNT_API_URL = os.getenv('API_BASE_URL') + '/update-account'
DELETE_ACCOUNT_API_URL = os.getenv('API_BASE_URL') + '/delete-account'

def main():
    st.title("View, Update, and Delete Accounts")

    # Initialize session state for selected account ID if it doesn't exist
    if 'selected_account_id' not in st.session_state:
        st.session_state.selected_account_id = None

    # Fetch accounts data from the API
    try:
        response = requests.get(GET_ACCOUNTS_API_URL)
        if response.status_code == 200:
            accounts_data = json.loads(response.content)
        else:
            st.error(f"Failed to fetch accounts: {response.status_code}")
            return
    except Exception as e:
        st.error(f"An error occurred while fetching accounts: {e}")
        return

    # Convert data to a DataFrame for better display
    accounts_df = pd.DataFrame(accounts_data)
    if accounts_df.empty:
        st.warning("No accounts found!")
        return

    # Display account information in a table format
    st.subheader("Accounts List")
    cols = st.columns([1, 1, 1, 1, 1.5])
    
    for col, title in zip(cols, ["Account Id", "Account Name", "Account Number", "Balance", "Actions"]):
        col.write(f"**{title}**")

    for index, row in accounts_df.iterrows():
        cols = st.columns([1, 1, 1, 1, 1.5])
        
        with cols[0]:
            st.write(row["id"])
        with cols[1]:
            st.write(row["account_name"])
        with cols[2]:
            st.write(row["account_number"])
        with cols[3]:
            st.write(row['balance'])  # Format balance as currency
        with cols[4]:
            column1,column2=st.columns(2)
            with column1:
                if st.button("Update", key=f"update_{row['id']}"):
                    st.session_state.selected_account_id = row["id"]  # Set the selected account ID for updating
            with column2:
                if st.button("Delete", key=f"delete_{row['id']}"):
                    delete_account(row["id"])

    # Check if an account is selected for updating
    if st.session_state.selected_account_id is not None:
        # Find the account details for the selected ID to display in the form
        account_to_update = accounts_df[accounts_df['id'] == st.session_state.selected_account_id].iloc[0]
        update_account(account_to_update)

    st.write("---")

def update_account(account):
    """Handle account update."""
    st.subheader(f"Updating account: {account['account_name']}")
    
    with st.form(f"update_form_{account['id']}"):
        new_name = st.text_input("Account Name", value=account["account_name"])
        new_account_number = st.text_input("Account Number", value=account["account_number"])
        new_balance = st.number_input("Balance", value=account["balance"], step=0.01, format="%.2f")
        submitted = st.form_submit_button("Submit")

        if submitted:
            payload = {
                "id": int(account["id"]),
                "account_name": new_name,
                "account_number": new_account_number,
                "balance": new_balance,
            }
            print(payload)  # This will print to your console/logs
            
            try:
                response = requests.put(UPDATE_ACCOUNT_API_URL, json=payload)
                if response.status_code == 200:
                    st.success("Account updated successfully!")
                    # Reset selected account ID after successful update
                    st.session_state.selected_account_id = None  
                    st.rerun()
                else:
                    st.error(f"Failed to update account: {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

def delete_account(account_id):
    """Handle account deletion."""
    try:
        payload={
            'id':account_id
        }
        response = requests.delete(f"{DELETE_ACCOUNT_API_URL}",json=payload)
        if response.status_code == 200:
            st.success("Account deleted successfully!")
            # Reset selected account ID after deletion
            st.session_state.selected_account_id = None  
            st.rerun()
        else:
            st.error(f"Failed to delete account: {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
