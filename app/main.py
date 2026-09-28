import os

import psycopg
from fastapi import FastAPI

app = FastAPI(title="CloudPulse API")

DATABASE_URL = os.getenv("DATABASE_URL")


@app.get("/")
def root():
    return {"message": "CloudPulse API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/health/db")
def database_health():
    try:
        with psycopg.connect(DATABASE_URL) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()

        return {
            "status": "healthy",
            "database": result[0],
        }

    except Exception as error:
        return {
            "status": "unhealthy",
            "error": str(error),
        }