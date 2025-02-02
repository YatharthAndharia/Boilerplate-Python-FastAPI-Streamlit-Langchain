from sqlalchemy import text
from fastapi import APIRouter,status,Request
from fastapi.responses import JSONResponse
from app.db.base_db import SessionLocal

router = APIRouter()

@router.get('/debt-summary')
async def get_debt_summary(
    request:Request,
):
    try:
        with SessionLocal() as db_conn:
            sql_txns = text(f"""
                SELECT 
                    t.id AS transaction_id,
                    t.transaction_date,
    	            fa.account_name AS from_account_name,
                    ta.account_name AS to_account_name,
                    t.transaction_amount,
                    t.remarks    
                FROM 
                    transactions t
                JOIN 
                    accounts fa ON t.from_account = fa.id
                JOIN 
                    accounts ta ON t.to_account = ta.id
                ORDER BY 
                    t.id ASC;
            """)
            sql_accounts=text(f"""
                SELECT * FROM accounts;
            """)
            result_txns = db_conn.execute(sql_txns)
            result_accounts=db_conn.execute(sql_accounts)
            txns=result_txns.fetchall()
            accounts=result_accounts.fetchall()
            

        owes_report= {account[1]: {} for account in accounts}
        for txn in txns:
            # Account that owes money
            debtor = txn[2]
            # Account that is owed money
            creditor = txn[3] 
            # Amount owed
            amount = float(txn[4])
            if debtor != creditor:
                if creditor in owes_report[debtor]:
                    owes_report[debtor][creditor] += amount
                else:
                    owes_report[debtor][creditor] = amount
        
        debtors=[]
        for debtor in owes_report.keys():
            debtors.append(debtor)

        for debtor in debtors:
            for item in owes_report:
                if debtor!=item:
                    if owes_report[debtor].get(item) and owes_report[item].get(debtor):
                        if owes_report[debtor][item]-owes_report[item][debtor]>=0:
                            owes_report[debtor][item] -= owes_report[item][debtor]                                
                            del owes_report[item][debtor]
        if owes_report!={}:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=owes_report
            )
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=""
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "ok": False,
                "detail": str(e),
            },
        )
