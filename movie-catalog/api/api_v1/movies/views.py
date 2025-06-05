from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

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
    exist_slug = next(
        (movie.slug for movie_item in MOVIES if movie_item.slug == movie.slug),
        None,
    )
    if not exist_slug:
        return Movie(**movie.model_dump())
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Movie with {movie.slug!r} slug already exists",
    )


@router.get(
    "/{slug}",
    response_model=Movie,
)
def read_movie(
    movie: Annotated[Movie, Depends(prefetch_movie)],
):
    return movie
