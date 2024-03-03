from typing import Any
from fastapi import FastAPI
from sqlmodel import Session
from app.database import create_db_and_tables, engine
from app.models import Activity, ActivityCreate, ActivityRead


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/activities/", response_model=ActivityRead)
async def create_activity(activity: ActivityCreate) -> Any:
    with Session(engine) as session:
        db_activity = Activity.model_validate(activity)
        session.add(db_activity)
        session.commit()
        session.refresh(db_activity)
        return db_activity
