from fastapi import FastAPI
import logging
from db_session import PostgresSingleton

app = FastAPI()


@app.get("/emergency_data")
def get_emergency_data():
    db = PostgresSingleton()
    data = db.execute_query("SELECT * FROM relief_locations;")
    return {"emergency_data": data}


@app.get("/health/db")
def db_health_check():
    """
    Database health check: returns "up" if query succeeds, otherwise "down".
    """
    try:
        db = PostgresSingleton()
        db.execute_query("SELECT 1;")
        return {"status": "up"}
    except Exception as e:
        logging.error(f"DB health check failed: {e}")
        return {"status": "down", "error": str(e)}
