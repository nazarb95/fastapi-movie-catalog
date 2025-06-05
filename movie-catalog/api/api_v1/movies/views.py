import random
from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.api_v1.movies.dependencies import (
    prefetch_movie,
)
from api.api_v1.movies.crud import MOVIES
from schemas.movies import (
    Movie,
    MovieCreate,
)

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


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(movie: MovieCreate):
    # generate a new id and checking its availability
    while True:
        movie_id = random.randint(1, 100)
        exist_movie_id = next(
            (movie.id for movie in MOVIES if movie.id == movie_id),
            None,
        )
        if not exist_movie_id:
            break

    return Movie(id=movie_id, **movie.model_dump())


@router.get(
    "/{movie_id}",
    response_model=Movie,
)
def read_movie(
    movie: Annotated[Movie, Depends(prefetch_movie)],
):
    return movie
