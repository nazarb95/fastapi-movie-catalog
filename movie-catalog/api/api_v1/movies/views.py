from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from api.api_v1.movies.dependencies import (
    prefetch_movie,
)
from api.api_v1.movies.crud import MOVIES
from schemas.movies import Movie

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[Movie],
)
def read_movies_list():
    return MOVIES


@router.get(
    "/{movie_id}",
    response_model=Movie,
)
def read_movie(
    movie: Annotated[Movie, Depends(prefetch_movie)],
):
    return movie
