from pydantic import BaseModel
from models.index import Users


class Note(BaseModel):
    title: str | None
    description: str | None
    read: bool = False
    user_id: int | None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        schema_extra = {}


class NoteList(Note):
    owner = Users

    class Config:
        orm_mode = True
