from sqlalchemy import text
from app.db.session import engine

def check_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
