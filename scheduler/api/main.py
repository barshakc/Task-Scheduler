from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from scheduler.db.database import get_db
from scheduler.celery_app import celery_app
from api.routers.route import router as task_router
from api.routers.auth import router as auth_router

app = FastAPI(title="Task Scheduler API")

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "error"

    try:
        celery_app.control.ping(timeout=1)
        celery_status = "ok"
    except Exception:
        celery_status = "error"

    return {
        "status": "ok",
        "db": db_status,
        "celery": celery_status
    }

app.include_router(auth_router)  
app.include_router(task_router)  
