from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import route  # your tasks router

app = FastAPI(title="Task Scheduler API")

# Include task routes
app.include_router(route.router)

# Serve frontend dashboard
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
