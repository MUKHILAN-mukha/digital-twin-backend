from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.check import check_db

app = FastAPI(title="Digital Twin Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "backend alive"}

@app.get("/db-check")
def db_check():
    try:
        check_db()
        return {"db": "connected"}
    except Exception as e:
        return {"db": "error", "detail": str(e)}
