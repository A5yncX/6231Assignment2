## comp6231assign2
```
├── comp6231.sqlite3     DataTable, include all the data
├── fruit_price_service  microservice for fruit_price
│   └── main.py
├── fruit_total_service  microservice for fruit_total_price
│   └── main.py
└── requirements.txt     Python Runtime Environment
```

## Command
```bash
# running fruit_price
uvicorn fruit_price_service.main:app --reload --port 8000
# running fruit_total
uvicorn fruit_total_service.main:app --reload --port 8100
```

## Requirements.txt

```
fastapi==0.100.0
uvicorn==0.23.2
httpx==0.24.1
pandas==2.1.0
```
