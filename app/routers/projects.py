from typing import Any, List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from app.database import engine
from app.models import (
    Project,
    ProjectCreate,
    ProjectUpdate,
    ProjectRead,
)

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post("/", response_model=ProjectRead)
async def create_project(project: ProjectCreate) -> Any:
    with Session(engine) as session:
        db_project = Project.model_validate(project)
        session.add(db_project)

        session.commit()
        session.refresh(db_project)

        return db_project


@router.get("/", response_model=List[ProjectRead])
async def read_projects() -> Any:
    with Session(engine) as session:
        statement = select(Project)
        results = session.exec(statement).all()

        return results


@router.get("/{id}", response_model=ProjectRead)
async def read_project(id: int) -> Any:
    with Session(engine) as session:
        project = session.get(Project, id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        return project


@router.put("/{id}", response_model=ProjectRead)
async def update_project(id: int, activity: ProjectUpdate):
    with Session(engine) as session:
        db_project = session.get(Project, id)
        if not db_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        project_data = activity.model_dump(exclude_unset=True)
        db_project.sqlmodel_update(project_data)

        session.add(db_project)
        session.commit()
        session.refresh(db_project)

        return db_project


@router.delete("/{id}", response_model=ProjectRead)
async def delete_project(id: int) -> Any:
    with Session(engine) as session:
        db_project = session.get(Project, id)
        if not db_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        session.delete(db_project)
        session.commit()

        return db_project
