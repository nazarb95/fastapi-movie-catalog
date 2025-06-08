from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from api.api_v1.movies.crud import MovieAlreadyExistsError, storage
from api.api_v1.movies.dependencies import (
    api_token_or_user_basic_auth_required_for_unsafe_methods,
)
from schemas.movies import (
    Movie,
    MovieCreate,
    MovieRead,
)

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[
        Depends(api_token_or_user_basic_auth_required_for_unsafe_methods),
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
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "A movie with such slug already exists.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie with slug='foobar' already exists.",
                    },
                },
            },
        },
    },
)
def create_movie(
    movie_create: MovieCreate,
) -> Movie:
    try:
        return storage.create_or_raise_if_exists(
            movie_in=movie_create,
        )
    except MovieAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Movie with slug={movie_create.slug!r} already exists.",
        ) from e
