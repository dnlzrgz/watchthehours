from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel


class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str]
    start_date: datetime
    end_date: Optional[datetime] = Field(default=None)


class ActivityCreate(SQLModel):
    name: str
    description: Optional[str] = None
    start_date: datetime


class ActivityUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ActivityRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
