from pathlib import Path

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from config.db import engine
from routes.index import user
from config.db import Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/media", StaticFiles(directory="media"), name="media")


app.include_router(user)
