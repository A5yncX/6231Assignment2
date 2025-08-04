import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import httpx

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Fruit Total Price Service")


PRICE_SERVICE_URL = "http://localhost:8000"

class TotalPriceResponse(BaseModel):
    fruit: str
    month: str
    fmp: float
    quantity: float
    total: float
    port: int

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
    "/fruit-total/fruit/{fruit}/month/{month}/quantity/{quantity}",
    response_model=TotalPriceResponse,
    summary="Get total price for a given fruit, month and quantity"
)
async def get_total_price(fruit: str, month: str, quantity: float, request: Request):
    price_data = await fetch_price_data(fruit, month)
    unit_price = price_data.get("fmp")
    total_price = unit_price * quantity
    return TotalPriceResponse(
        fruit=fruit.lower(),
        month=month.lower(),
        fmp=unit_price,
        quantity=quantity,
        total=total_price,
        port=request.url.port
    )
