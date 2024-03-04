from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import activities, projects


app = FastAPI()
app.include_router(activities.router)
app.include_router(projects.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
