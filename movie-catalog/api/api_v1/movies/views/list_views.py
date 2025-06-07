from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from api.api_v1.movies.dependencies import (
    exists_slug_movie,
    save_storage_state,
    api_token_required_for_unsafe_methods,
    user_basic_auth_required_for_unsafe_methods,
)
from api.api_v1.movies.crud import storage
from schemas.movies import (
    Movie,
    MovieCreate,
    MovieRead,
)

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[
        Depends(save_storage_state),
        Depends(user_basic_auth_required_for_unsafe_methods),
        # Depends(api_token_required_for_unsafe_methods),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    },
                },
            },
        },
    },
)


@router.get(
    "/",
    response_model=list[MovieRead],
)
def read_movies_list() -> list[Movie]:
    return storage.get()


@router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie_create: Annotated[
        MovieCreate,
        Depends(exists_slug_movie),
    ],
) -> Movie:
    return storage.create(movie_in=movie_create)
