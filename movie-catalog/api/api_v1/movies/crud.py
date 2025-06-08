import logging

from pydantic import BaseModel, ValidationError
from redis import Redis

from core import config
from core.config import MOVIE_STORAGE_FILE_PATH
from schemas.movies import Movie, MovieCreate, MovieUpdate

logger = logging.getLogger(__name__)


redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_MOVIES,
    decode_responses=True,
)


class MovieStorage(BaseModel):
    slug_movie: dict[str, Movie] = {}

    def save_state(self) -> None:
        MOVIE_STORAGE_FILE_PATH.write_text(self.model_dump_json(indent=2))
        logger.info("Saved movies to storage file")

    @classmethod
    def from_state(cls) -> "MovieStorage":
        if not MOVIE_STORAGE_FILE_PATH.exists():
            logger.info("Movies file does not exist")
            return MovieStorage()
        return cls.model_validate_json(MOVIE_STORAGE_FILE_PATH.read_text())

    def init_storage_from_state(self) -> None:
        try:
            data = MovieStorage.from_state()
        except ValidationError:
            self.save_state()
            logger.warning("Rewritten storage file due to validation error.")
            return

        storage.slug_movie.update(data.slug_movie)
        logger.warning("Recovered data from storage file")

    def get(self) -> list[Movie]:
        return list(
            map(
                Movie.model_validate_json,
                redis.hvals(
                    config.REDIS_MOVIE_HASH_HAME,
                ),
            )
        )

    def get_by_slug(self, slug: str) -> Movie | None:
        data = redis.hget(config.REDIS_MOVIE_HASH_HAME, slug)
        if not data:
            return None
        return Movie.model_validate_json(data)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(
            **movie_in.model_dump(),
        )
        redis.hset(
            name=config.REDIS_MOVIE_HASH_HAME,
            key=movie.slug,
            value=movie.model_dump_json(),
        )
        logger.info("Created movie %s", movie.slug)
        return movie

    def delete_by_slug(self, slug: str) -> None:
        self.slug_movie.pop(slug, None)

    def delete(self, movie: Movie) -> None:
        self.delete_by_slug(slug=movie.slug)

    def update(
        self,
        movie: Movie,
        movie_in: MovieUpdate,
    ) -> Movie:
        for field_name, value in movie_in:
            setattr(movie, field_name, value)

        return movie

    def update_partial(self, movie: Movie, movie_in: MovieUpdate) -> Movie:
        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)
        return movie


storage = MovieStorage()
