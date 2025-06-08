from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    # actions before the application
    # tarts pause this function while the application is running
    yield
    # perform shutdown,
    # close the connections, and finally save the files.
