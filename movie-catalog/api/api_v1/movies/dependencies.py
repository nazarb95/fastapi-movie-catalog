import logging
from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
    Depends,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from api.api_v1.movies.crud import storage
from core.config import API_TOKENS
from schemas.movies import Movie, MovieCreate


logger = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)

statis_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your **Static API token** from developer portal",
    auto_error=False,
)


def prefetch_movie(
    slug: str,
) -> Movie:
    movie_item: Movie | None = storage.get_by_slug(slug=slug)
    if movie_item:
        return movie_item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with {slug!r} not found",
    )


def exists_slug_movie(
    movie: MovieCreate,
) -> MovieCreate:
    exist_slug = storage.get_by_slug(movie.slug)

    if not exist_slug:
        return movie
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Movie with {movie.slug!r} slug already exists",
    )


def save_storage_state(
    request: Request,
    background_task: BackgroundTasks,
):
    # first the code before going inside the view function
    yield
    # code after leaving the view function
    if request.method in UNSAFE_METHODS:
        logger.info("Add background task to save storage")
        background_task.add_task(storage.save_state)


def api_token_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(statis_api_token),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )

    if api_token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )
