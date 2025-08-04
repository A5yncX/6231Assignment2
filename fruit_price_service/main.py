import sqlite3
import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "comp6231.sqlite3"

ALLOWED_MONTHS = {
    "jan", "feb", "mar", "apr", "may", "jun",
    "jul", "aug", "sep", "oct", "nov", "dec"
}

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Fruit Month Price Service")


class PriceResponse(BaseModel):
    fruit: str
    month: str
    fmp: float
    port: int


def query_price(fruit: str, month: str) -> float:
    if month not in ALLOWED_MONTHS:
        raise HTTPException(status_code=400, detail=f"Invalid month: {month}")
    try:
        conn = sqlite3.connect(str(DATABASE_PATH))
        cursor = conn.cursor()
        sql = f'SELECT "{month.capitalize()}" FROM FMP WHERE FRUIT = ? COLLATE NOCASE'
        cursor.execute(sql, (fruit,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Fruit or month not found")
        return row[0]
    except sqlite3.OperationalError as e:
        logging.error(f"SQLite operational error: {e}")
        raise HTTPException(status_code=500, detail="Database schema error")
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
        raise HTTPException(status_code=500, detail="Internal database error")


@app.get(
    "/fruit-price/fruit/{fruit}/month/{month}",
    response_model=PriceResponse,
    summary="Get unit price for a given fruit in a given month"
)
async def get_fruit_price(fruit: str, month: str, request: Request):
    fruit_lower = fruit.lower()
    month_lower = month.lower()
    price = query_price(fruit_lower, month_lower)
    return PriceResponse(
        fruit=fruit_lower,
        month=month_lower,
        fmp=price,
        port=request.url.port
    )
