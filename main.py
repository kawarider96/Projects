from contextlib import asynccontextmanager
from fastapi import FastAPI
from Global.Dependencies import db
from Routes.Routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()

    yield

    db.close()


app = FastAPI(
    title="Project Manager API",
    version="1.0.0",
    description="API for the Project Manager application.",
    lifespan=lifespan,
)

app.include_router(router)