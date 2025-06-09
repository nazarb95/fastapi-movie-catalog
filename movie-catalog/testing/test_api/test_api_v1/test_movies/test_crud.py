import random
import string
from os import getenv
from typing import ClassVar
from unittest import TestCase

from api.api_v1.movies.crud import storage
from schemas.movies import Movie, MovieCreate, MoviePartialUpdate, MovieUpdate

if getenv("TESTING") != "1":
    raise OSError(  # noqa: TRY003
        "Environment is not ready for testing",  # noqa: EM101
    )


def create_movie() -> Movie:
    movie_in = MovieCreate(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=8,
            ),
        ),
        title="Test Movie",
        description="Test Movie Description",
        year=2020,
        genre="Action",
    )
    return storage.create(movie_in=movie_in)


class MovieStorageUpdateTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = create_movie()

    def tearDown(self) -> None:
        storage.delete(self.movie)

    def test_update(self) -> None:
        movie_update = MovieUpdate(
            **self.movie.model_dump(),
        )
        source_description = self.movie.description
        movie_update.description *= 2
        updated_movie = storage.update(
            movie=self.movie,
            movie_in=movie_update,
        )
        self.assertNotEqual(
            source_description,
            updated_movie.description,
        )
        self.assertEqual(
            movie_update,
            MovieUpdate(**updated_movie.model_dump()),
        )

    def test_update_partial(self) -> None:
        movie_partial_update = MoviePartialUpdate(
            description=self.movie.description * 2,
        )
        source_description = self.movie.description
        updated_movie = storage.update_partial(
            movie=self.movie,
            movie_in=movie_partial_update,
        )

        self.assertNotEqual(
            source_description,
            updated_movie.description,
        )
        self.assertEqual(
            movie_partial_update.description,
            updated_movie.description,
        )


class MovieStorageGetMeviesTestCase(TestCase):
    MOVIES_COUNT = 3
    movies: ClassVar[list[Movie]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.movies = [create_movie() for _ in range(cls.MOVIES_COUNT)]

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies:
            storage.delete(movie)

    def test_get_list(self) -> None:
        movies = storage.get()
        expected_slugs = {movie.slug for movie in self.movies}
        slugs = {movie.slug for movie in movies}
        expected_diff = set[str]()
        diff = expected_slugs - slugs
        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for movie in self.movies:
            with self.subTest(
                slug=movie.slug,
                msg=f"Validate can get slug {movie.slug!r}",
            ):
                db_movie = storage.get_by_slug(slug=movie.slug)
                self.assertEqual(
                    movie,
                    db_movie,
                )
