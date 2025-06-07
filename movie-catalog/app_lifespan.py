from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.api_v1.movies.crud import storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    # actions before the application
    storage.init_storage_from_state()
    # tarts pause this function while the application is running
    yield
    # perform shutdown,
    # close the connections, and finally save the files.
