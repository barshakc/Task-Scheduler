from fastapi import FastAPI
from routers.route import router as tasks_router

app = FastAPI(title="Task Scheduler API")

app.include_router(tasks_router)
