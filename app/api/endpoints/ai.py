from sqlalchemy import text
from fastapi import APIRouter,status,Request
from fastapi.responses import JSONResponse
from app.utils.helper import serialize_account_data
from app.db.base_db import SessionLocal
from app.pydantic.ai import AIRequest
from app.prompts.prompts import NATURAL_LANGUAGE_ANSWER_PROMPT
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()

postgres_connection_uri=f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

db = SQLDatabase.from_uri(postgres_connection_uri)
llm_sql = ChatOpenAI(model=os.getenv('OPENAI_GPT_3.5_TURBO'), temperature=0,api_key=os.getenv('OPENAI_API_KEY'))
llm=ChatOpenAI(model=os.getenv('OPENAI_GPT_4O_MINI'), temperature=0,api_key=os.getenv('OPENAI_API_KEY'))

@router.post('/ai-bot')
async def add_account(
    request:Request,
    request_params:AIRequest
):
    """
        API endpoint for ai-bot
    """
    try:
        question=request_params.question
        print("Question:",question)
        
        chain = create_sql_query_chain(llm_sql, db)
        response = chain.invoke({"question": question})
        print(response)
        answer=db.run(response)
        print("Answer:",answer,"@@@@@@@@@@@")
        nl_chain=NATURAL_LANGUAGE_ANSWER_PROMPT | llm
        nl_response=nl_chain.invoke({'user_question':question,'query_results':answer})
        # print(nl_response.content['ai_answer'],"!!!!!!!!!!!!")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=nl_response.content   
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
