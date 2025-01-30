from sqlalchemy import text
from fastapi import APIRouter,status,Request
from fastapi.responses import JSONResponse
from app.utils.helper import serialize_account_data
from app.db.base_db import SessionLocal
from app.pydantic.accounts import AddAccountRequest,UpdateAccountRequest,DeleteAccountRequest
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

@router.post('/add-account')
async def add_account(
    request:Request,
    request_params:AddAccountRequest
):
    """
        API for adding account in master
    """
    account_name=request_params.account_name
    account_number=request_params.account_number
    balance=request_params.balance
    try:
        with SessionLocal() as db_conn:
            sql = text(f"""
                INSERT INTO accounts (account_name, account_number, balance)
                VALUES (:account_name, :account_number, :balance)
            """)
            db_conn.execute(sql,{'account_name':account_name,'account_number':account_number,'balance':balance})
            db_conn.commit()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "ok": True,
                "detail": "account added successfully",
            },
    )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "ok": False,
                "detail": str(e),
            },
        )
    
@router.get('/get-accounts')
async def get_account():
    """
        API for getting all accounts
    """
    try:
        with SessionLocal() as db_conn:
            sql = text(f"""
                SELECT id,account_name,account_number,balance FROM accounts ORDER BY id ASC
            """)
            result = db_conn.execute(sql)
            data=result.fetchall()
            data=serialize_account_data(data)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=data
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

@router.put('/update-account')
async def update_account(
    request:Request,
    request_params:UpdateAccountRequest
):
    """
        API for updating an existing account
    """
    try:
        id=request_params.id
        account_name=request_params.account_name
        account_number=request_params.account_number
        balance=request_params.balance

        with SessionLocal() as db_conn:
            sql = text(f"""
                UPDATE accounts 
                SET account_name=:account_name, account_number=:account_number, balance=:balance, updated_at=CURRENT_TIMESTAMP
                WHERE id=:id"""
            )
            db_conn.execute(sql,{'account_name':account_name,'account_number':account_number,'balance':balance,'id':id})
            db_conn.commit()
                       
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "ok": False,
                "detail": str(e),
            },
        )
    
@router.delete('/delete-account')
async def delete_account(
    request:Request,
    request_params:DeleteAccountRequest
):
    """
        API for deleting an existing account
    """
    try:
        id=request_params.id
        with SessionLocal() as db_conn:
            sql = text(f"""DELETE FROM accounts 
                WHERE id=:id"""
            )
            db_conn.execute(sql,{'id':id})
            db_conn.commit()
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "ok": False,
                "detail": str(e),
            },
        )