from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel


class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str]
    color: int

    activities: List["Activity"] = Relationship(back_populates="project")


class ProjectCreate(SQLModel):
    name: str
    description: Optional[str] = None
    color: int


class ProjectUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[int] = None


class ProjectRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    color: int


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str]
    start_date: datetime
    end_date: Optional[datetime] = Field(default=None)

    project_id: Optional[int] = Field(default=None, foreign_key="project.id")
    project: Optional[Project] = Relationship(back_populates="activities")


class ActivityCreate(SQLModel):
    name: str
    description: Optional[str] = None
    start_date: datetime
    project: Optional[int] = None


class ActivityUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    project_id: Optional[int] = None


class ActivityRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    project_id: Optional[int] = None
