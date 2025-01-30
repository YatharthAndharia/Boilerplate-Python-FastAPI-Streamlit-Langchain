import streamlit as st
import pandas as pd
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path(__file__).resolve().parent.parent.parent / "streamlit.env"

load_dotenv(dotenv_path)

# API URLs (replace with your actual API endpoints)
GET_TXNS_API_URL = os.getenv('API_BASE_URL') + '/get-transactions'
UPDATE_TXN_API_URL = os.getenv('API_BASE_URL') + '/update-transaction'
DELETE_TXN_API_URL = os.getenv('API_BASE_URL') + '/delete-transaction'
GET_ACCOUNTS_API_URL = os.getenv('API_BASE_URL') + '/get-accounts'

def main():
    st.title("View, Update, and Delete Transactions")

    # Initialize session state variables
    if 'selected_txn_id' not in st.session_state:
        st.session_state.selected_txn_id = None
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0  # Start with the first page

    # Fetch transactions data from the API
    try:
        response = requests.get(GET_TXNS_API_URL)
        if response.status_code == 200:
            txns_data = json.loads(response.content)
        else:
            st.error(f"Failed to fetch transactions: {response.status_code}")
            return
    except Exception as e:
        st.error(f"An error occurred while fetching transactions: {e}")
        return

    # Convert data to a DataFrame for better display
    txns_df = pd.DataFrame(txns_data)
    if txns_df.empty:
        st.warning("No transactions found!")
        return

    # Pagination logic
    items_per_page = 10
    total_pages = (len(txns_df) - 1) // items_per_page + 1
    start_idx = st.session_state.page_number * items_per_page
    end_idx = start_idx + items_per_page
    current_page_data = txns_df.iloc[start_idx:end_idx]

    # Display transactions with pagination
    
    cols = st.columns([0.5, 2, 1.5, 1.5, 1.7, 2, 3.5])

    for col, title in zip(cols, ["Id", "Txn Date", "From", "To", "Amount", "Remarks", "Actions"]):
        col.write(f"**{title}**")

    for index, row in current_page_data.iterrows():
        cols = st.columns([0.5, 2, 1.5, 1.5, 1.7, 2, 3.5])

        with cols[0]:
            st.write(row["id"])
        with cols[1]:
            st.write(datetime.strptime(row['transaction_date'], "%Y-%m-%dT%H:%M:%S").date())
        with cols[2]:
            st.write(row["from_account"])
        with cols[3]:
            st.write(row['to_account'])
        with cols[4]:
            st.write(row['transaction_amount'])
        with cols[5]:
            st.write(row['remarks'])
        with cols[6]:
            column1, column2 = st.columns(2)
            with column1:
                if st.button("Update", key=f"update_{row['id']}"):
                    st.session_state.selected_txn_id = row["id"]
            with column2:
                if st.button("Delete", key=f"delete_{row['id']}"):
                    delete_account(row["id"])

    # Pagination controls
    st.markdown(
        f'<div style="text-align: right;">(Page {st.session_state.page_number + 1} of {total_pages})</div>',
        unsafe_allow_html=True
    )
    st.write("---")
    prev, next = st.columns([100,7])

    with prev:

        st.button("Previous", 
                  disabled=st.session_state.page_number == 0, 
                  on_click=lambda: st.session_state.update(page_number=st.session_state.page_number - 1))

    with next:
        st.button("Next", 
                  disabled=st.session_state.page_number >= total_pages - 1, 
                  on_click=lambda: st.session_state.update(page_number=st.session_state.page_number + 1))

    # Check if a transaction is selected for updating
    if st.session_state.selected_txn_id is not None:
        transaction_to_update = txns_df[txns_df['id'] == st.session_state.selected_txn_id].iloc[0]
        update_transaction(transaction_to_update)



def update_transaction(transaction):
    """Handle transaction update with dropdowns for accounts."""

    # Fetch accounts for dropdowns
    try:
        response = requests.get(GET_ACCOUNTS_API_URL)
        if response.status_code == 200:
            accounts_data = response.json()  # Assuming API returns a JSON array of accounts
            account_options = {account["id"]: account["account_name"] for account in accounts_data}
            account_options_id = {account["account_name"]: account["id"] for account in accounts_data}
        else:
            st.error(f"Failed to fetch accounts: {response.status_code}")
            return
    except Exception as e:
        st.error(f"An error occurred while fetching accounts: {e}")
        return

    with st.form(f"update_form_{transaction['id']}"):
        # Dropdowns for From Account and To Account
        st.write("**Update Transaction** :",str(transaction['id']))
        new_from_account = st.selectbox(
            "From Account",
            options=list(account_options.values()),
            index=list(account_options.values()).index(transaction["from_account"]),
            help="Select the account from which the funds were transferred.",
        )
        new_to_account = st.selectbox(
            "To Account",
            options=list(account_options.values()),
            index=list(account_options.values()).index(transaction["to_account"]),
            help="Select the account to which the funds were transferred.",
        )
        new_transaction_amount = st.number_input(
            "Transaction Amount",
            value=float(transaction["transaction_amount"]),
            step=0.01,
            format="%.2f",
            help="Enter the new transaction amount.",
        )
        new_transaction_date = st.date_input(
            "Transaction Date",
            value=pd.to_datetime(transaction["transaction_date"]),
            help="Select the new transaction date.",
        )
        new_remarks=st.text_input(
            "Remarks",
            value=transaction['remarks'],
            help="Enter the new remarks"      
        )
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Ensure From Account and To Account are not the same
            if new_from_account == new_to_account:
                st.error("From Account and To Account cannot be the same.")
                return

            # Prepare the payload
            payload = {
                "id": int(transaction["id"]),
                "from_account": account_options_id[new_from_account],
                "to_account": account_options_id[new_to_account],
                "transaction_amount": new_transaction_amount,
                "transaction_date": str(new_transaction_date),
                "remarks":new_remarks
            }

            try:
                # Send the update request to the API
                response = requests.put(UPDATE_TXN_API_URL, json=payload)
                if response.status_code == 200:
                    st.success("Transaction updated successfully!")
                    # Reset selected transaction ID after successful update
                    st.session_state.selected_txn_id = None  
                    st.rerun()
                else:
                    st.error(f"Failed to update transaction: {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")



def delete_account(account_id):
    """Handle transaction deletion."""
    try:
        payload={
            'id':account_id
        }
        response = requests.delete(f"{DELETE_TXN_API_URL}",json=payload)
        if response.status_code == 200:
            st.success("Account deleted successfully!")
            # Reset selected account ID after deletion
            st.session_state.selected_txn_id = None  
            st.rerun()
        else:
            st.error(f"Failed to delete account: {response.text}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
