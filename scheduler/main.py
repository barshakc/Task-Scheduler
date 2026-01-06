from fastapi import FastAPI
from routers.route import router as tasks_router
from db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Scheduler API")
app.include_router(tasks_router)
