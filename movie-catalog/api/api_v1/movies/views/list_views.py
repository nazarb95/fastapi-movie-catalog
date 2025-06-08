from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
)

from api.api_v1.movies.dependencies import (
    api_token_or_user_basic_auth_required_for_unsafe_methods,
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
)
def create_movie(
    movie_create: MovieCreate,
) -> Movie:
    if not storage.get_by_slug(movie_create.slug):
        return storage.create(movie_in=movie_create)
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Movie with slug={movie_create.slug!r} already exists.",
    )
