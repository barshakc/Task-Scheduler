from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import route  

app = FastAPI(title="Task Scheduler API")

app.include_router(route.router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
