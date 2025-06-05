from fastapi import HTTPException
from starlette import status

from api.api_v1.movies.crud import MOVIES
from schemas.movies import Movie


def prefetch_movie(
    slug: str,
) -> Movie:
    movie_item = next(
        (movie for movie in MOVIES if movie.slug == slug),
        None,
    )
    if movie_item:
        return movie_item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie with {slug!r} not found",
    )
