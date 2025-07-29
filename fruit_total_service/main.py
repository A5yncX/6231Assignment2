# fruit_total_service/main.py
import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import httpx
from itertools import count

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Fruit Total Price Service")

# 价格服务地址
PRICE_SERVICE_URL = "http://localhost:9000"

# 全局计数器，首次调用时 id=10001，后续递增
total_id_counter = count(10001)

class TotalPriceResponse(BaseModel):
    id: int
    fruit: str
    month: str
    Emp: float
    quantity: float
    totalPrice: float
    environmet: str

async def fetch_price_data(fruit: str, month: str) -> dict:
    fruit_lower = fruit.lower()
    month_lower = month.lower()
    url = f"{PRICE_SERVICE_URL}/fruit-price/fruit/{fruit_lower}/month/{month_lower}"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=5.0)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logging.exception("Error calling price service")
        raise HTTPException(status_code=500, detail=f"Cannot reach price service: {e}")

@app.get(
    "/fruit-total-price/fruit/{fruit}/month/{month}/quantity/{quantity}",
    response_model=TotalPriceResponse,
    summary="Get total price for a given fruit, month and quantity"
)
async def get_total_price(fruit: str, month: str, quantity: float, request: Request):
    # 生成本次请求的唯一 ID
    id_value = next(total_id_counter)
    # 从价格服务获取数据
    price_data = await fetch_price_data(fruit, month)
    unit_price = price_data.get("fmp")
    # 动态获取当前端口号
    environment = str(request.url.port)
    total_price = unit_price * quantity

    return TotalPriceResponse(
        id=id_value,
        fruit=fruit.lower(),
        month=month.lower(),
        Emp=unit_price,
        quantity=quantity,
        totalPrice=total_price,
        environmet=environment
    )
