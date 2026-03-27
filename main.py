from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
import base64
import os
from dotenv import load_dotenv

load_dotenv() # .env 파일을 읽음

app = FastAPI()

TOSS_SECRET_KEY = os.getenv("TOSS_SECRET_KEY")

#index.html 서빙
@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", encoding="utf-8") as f:
        return f.read()
    
#결제 성공 콜백
@app.get("/success")
async def success(paymentKey: str, orderId: str, amount: int):
    url = f"https://api.tosspayments.com/v1/payments/{paymentKey}"

    #Basic AUth 인코딩
    secret = base64.b64encode(f"{TOSS_SECRET_KEY}:".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {secret}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        
        return JSONResponse(content=response.json())
    
#결제 실패 콜백
@app.get("/fail")
async def fail(code: str,  message:str, orderId: str):
    return JSONResponse(content={
        "code": code,
        "message": message,
        "orderId": orderId
    })