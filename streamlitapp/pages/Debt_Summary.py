import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime, date
from decimal import Decimal
from dotenv import load_dotenv
load_dotenv()

DEBT_SUMMARY_API_URL = os.getenv('API_BASE_URL')+ '/debt-summary'

def main():
    try:
        
        st.write(f"**Debt Summary** ({str(date.today())})")
        response = requests.get(DEBT_SUMMARY_API_URL)
        if response.status_code == 200:
            owes_data = response.json()
            final_answer=[]
            for payer, payees in owes_data.items():
                for payee, amount in payees.items():
                    final_answer.append({'payer': payer, 'payee': payee, 'amount': Decimal(amount)})
            df = pd.DataFrame(final_answer)
            st.table(df)
        else:
            st.error(f"Failed to fetch report: {response.content}")
            return
    except Exception as e:
        st.error(f"An error occurred while fetching report: {e}")
        return

if __name__ == "__main__":
    main()