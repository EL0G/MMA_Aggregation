import os
from dotenv import load_dotenv
import psycopg
import datetime

load_dotenv()

db_host = os.getenv("HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_port = os.getenv("DB_PORT")

conn = psycopg.connect(
    host=db_host, dbname=db_name, user=db_user, password=db_pass, port=db_port
)

if __name__ == "__main__":
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE MMA_events (
            id SERIAL PRIMARY KEY,
            event_name VARCHAR(255),
            event_date DATE,
            UNIQUE (event_name, event_date)
        )
    """)
    conn.commit()
