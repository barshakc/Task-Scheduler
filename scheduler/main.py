from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.route import router as task_router
from routers.auth import router as auth_router

app = FastAPI(title="Task Scheduler API")

app.include_router(auth_router) 
app.include_router(task_router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
