from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # actions before the application
    # tarts pause this function while the application is running
    yield
    # perform shutdown,
    # close the connections, and finally save the files.
