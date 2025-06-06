from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from api.api_v1.movies.dependencies import (
    prefetch_movie,
    exists_slug_movie,
)
from api.api_v1.movies.crud import storage
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
def read_movies_list() -> list[Movie]:
    return storage.get()


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie: Annotated[
        MovieCreate,
        Depends(exists_slug_movie),
    ],
) -> Movie:
    return storage.create(movie_in=movie)


@router.get(
    "/{slug}/",
    response_model=Movie,
)
def read_movie(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie),
    ],
) -> Movie:
    return movie


@router.delete(
    "/{slug}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie 'slug' not found",
                    },
                },
            },
        },
    },
)
def delete_movie(
    movie: Annotated[
        Movie,
        Depends(prefetch_movie),
    ],
):
    storage.delete(movie=movie)
