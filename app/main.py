from datetime import datetime, timezone
from typing import Any, List
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from app.database import create_db_and_tables, engine
from app.models import (
    Activity,
    ActivityCreate,
    ActivityUpdate,
    ActivityRead,
)


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


@app.get("/activities/", response_model=List[ActivityRead])
async def read_activities() -> Any:
    with Session(engine) as session:
        statement = select(Activity)
        results = session.exec(statement).all()

        return results


@app.get("/activities/{id}", response_model=ActivityRead)
async def read_activity(id: int) -> Any:
    with Session(engine) as session:
        activity = session.get(Activity, id)
        if not activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity not found",
            )

        return activity


@app.put("/activities/{id}", response_model=ActivityRead)
async def update_activity(id: int, activity: ActivityUpdate):
    with Session(engine) as session:
        db_activity = session.get(Activity, id)
        if not db_activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity not found",
            )

        activity_data = activity.model_dump(exclude_unset=True)
        db_activity.sqlmodel_update(activity_data)

        session.add(db_activity)
        session.commit()
        session.refresh(db_activity)

        return db_activity


@app.delete("/activities/{id}", response_model=ActivityRead)
async def delete_activity(id: int) -> Any:
    with Session(engine) as session:
        db_activity = session.get(Activity, id)
        if not db_activity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Activity not found",
            )
        session.delete(db_activity)
        session.commit()

        return db_activity


@app.post("/activities/start", response_model=ActivityRead)
async def start_activity(name: str) -> Any:
    with Session(engine) as session:
        activity = ActivityCreate(
            name=name,
            start_date=datetime.now(),
        )
        db_activity = Activity.model_validate(activity)
        session.add(db_activity)

        session.commit()
        session.refresh(db_activity)

        return db_activity


@app.post("/activities/stop/", response_model=ActivityRead)
async def stop_activity() -> Any:
    with Session(engine) as session:
        statement = select(Activity).where(Activity.end_date == None)
        result = session.exec(statement).first()

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No ongoing activity found",
            )

        result.end_date = datetime.now(timezone.utc)

        session.add(result)
        session.commit()
        session.refresh(result)

        return result
