from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.check import router as db_check_router
from app.db.check import db_check as check_db
from app.routers.auth import router as auth_router

app = FastAPI(title="Digital Twin Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(db_check_router)
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
