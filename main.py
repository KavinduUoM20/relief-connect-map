from fastapi import FastAPI
import logging
from db_session import PostgresSingleton

app = FastAPI()


@app.get("/locations")
def get_locations():
    data = [
        {"id": 1, "name": "Colombo", "status": "safe"},
        {"id": 2, "name": "Gampaha", "status": "flooded"},
        {"id": 3, "name": "Kegalle", "status": "warning"},
    ]
    return {"locations": data}


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
