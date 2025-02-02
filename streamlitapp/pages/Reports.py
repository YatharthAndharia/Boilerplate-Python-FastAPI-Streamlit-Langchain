# import streamlit as st
# import requests
# import pandas as pd
# import os
# from datetime import datetime, date
# from dotenv import load_dotenv
# load_dotenv()

# # API URL to fetch accounts (replace with your actual endpoint)
# GET_ACCOUNTS_API_URL = os.getenv('API_BASE_URL') + '/get-accounts'
# GET_TRANSACTIONS_API_URL = os.getenv('API_BASE_URL') + '/get-transactions'

# def main():
#     st.title("Transaction Reports")

#     # Fetch accounts for dropdowns
#     try:
#         response = requests.get(GET_ACCOUNTS_API_URL)
#         if response.status_code == 200:
#             accounts_data = response.json()  # Assuming API returns a JSON array of accounts
#             account_options = {account["account_name"]: account["id"] for account in accounts_data}
#         else:
#             st.error(f"Failed to fetch accounts: {response.status_code}")
#             return
#     except Exception as e:
#         st.error(f"An error occurred while fetching accounts: {e}")
#         return

#     # Filters for reports
#     st.subheader("Filter Transactions")
#     with st.form("filter_form"):
#         # transaction_date_from = st.date_input(
#         #     "Transaction Date From",
#         #     help="Select the start date for filtering transactions."
#         # )
#         # transaction_date_to = st.date_input(
#         #     "Transaction Date To",
#         #     help="Select the end date for filtering transactions."
#         # )
#         from_account = st.selectbox(
#             "From Account",
#             options=["All"] + list(account_options.keys()),
#             help="Select the account from which funds were transferred. Choose 'All' to include all accounts.",
#         )
#         to_account = st.selectbox(
#             "To Account",
#             options=["All"] + list(account_options.keys()),
#             help="Select the account to which funds were transferred. Choose 'All' to include all accounts.",
#         )

#         # Submit button
#         submitted = st.form_submit_button("Generate Report")

#     # Handle filter submission
#     if submitted:
#         # Prepare query parameters for API
#         filters = {
#             "transaction_date_from": str(transaction_date_from),
#             "transaction_date_to": str(transaction_date_to),
#             "from_account": account_options.get(from_account) if from_account != "All" else None,
#             "to_account": account_options.get(to_account) if to_account != "All" else None,
#         }

#         try:
#             # Fetch filtered transactions
#             response = requests.get(GET_TRANSACTIONS_API_URL, params=filters)
#             if response.status_code == 200:
#                 transactions = response.json()  # Assuming API returns a JSON array of transactions
#                 if transactions:
#                     # Convert data to a DataFrame for better display
#                     df = pd.DataFrame(transactions)
#                     st.subheader("Transaction Report")
#                     st.dataframe(df)
#                 else:
#                     st.warning("No transactions found for the selected filters.")
#             else:
#                 st.error(f"Failed to fetch transactions: {response.status_code}")
#         except Exception as e:
#             st.error(f"An error occurred while fetching transactions: {e}")

# if __name__ == "__main__":
#     main()
