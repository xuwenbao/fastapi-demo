from typing import Optional

from sqlmodel import Field, SQLModel


class DioceseBase(SQLModel):
    name: str = Field(index=True, sa_column_kwargs={"unique": True})


class Diocese(DioceseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


### DIOCESE RESOURCE MODELS
class DioceseCreate(DioceseBase):
    pass


class DioceseRead(DioceseBase):
    id: int


class DioceseUpdate(SQLModel):
    name: Optional[str]
