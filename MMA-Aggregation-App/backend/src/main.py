from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models.database import conn

app = FastAPI()


class Item(BaseModel):
    event_name: str
    event_date: date


@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "message": "Welcome to the MMA Aggregation API. Go to /docs for interactive testing.",
    }


@app.get("/events")
def get_all_events():
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT event_name, event_date FROM mma_events")
            rows = cur.fetchall()

            events = []
            for row in rows:
                events.append(Item(event_name=str(row[0]), event_date=row[1]))
            return events

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database operational error: {str(e)}"
        )

