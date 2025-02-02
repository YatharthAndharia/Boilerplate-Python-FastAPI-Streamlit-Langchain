import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime, date
from decimal import Decimal
from pathlib import Path
from dotenv import load_dotenv
dotenv_path = Path(__file__).resolve().parent.parent / "streamlit.env"
load_dotenv(dotenv_path)

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
            df=df.sort_values(by='payer')
            st.table(df)
        else:
            st.warning(f"Summary not found.")
            return
    except Exception as e:
        st.error(f"An error occurred while fetching report: {e}")
        return

if __name__ == "__main__":
    main()