from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routers.route import router as task_router
from api.routers.auth import router as auth_router
from pathlib import Path

app = FastAPI(title="Task Scheduler API")

app.include_router(auth_router)
app.include_router(task_router)


