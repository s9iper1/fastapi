from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from config.db import engine
from routes.index import user
from config.db import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/media", StaticFiles(directory="media"), name="media")


app.include_router(user)

# students = {
#     1: {
#         "name": "Bilal",
#         "age": 30
#     }
# }
#
#
# @app.get("/")
# def index():
#     return {"name": "This is a name"}
#
#
# @app.get("/get-student/{student_id}")
# def get_student(student_id: int = Path(None, description='The id of the student you want to view')):
#     if student_id in students:
#         return students[student_id]
#     else:
#         return "Student does not exist"
