import logging

from fastapi import HTTPException, BackgroundTasks
from starlette import status

from api.api_v1.movies.crud import storage
from schemas.movies import Movie, MovieCreate


logger = logging.getLogger(__name__)


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
    background_task: BackgroundTasks,
):
    # first the code before going inside the view function
    yield
    # code after leaving the view function
    logger.info("Add background task to save storage")
    background_task.add_task(storage.save_state)
