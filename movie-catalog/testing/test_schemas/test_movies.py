from unittest import TestCase

from schemas.movies import Movie, MovieCreate, MoviePartialUpdate, MovieUpdate


class MovieTestCase(TestCase):
    def test_movie_can_be_created_from_create_schema(self) -> None:
        movie_in = MovieCreate(
            slug="some-slug",
            description="Some description",
            title="Some title",
            year=2025,
            genre="Some genre",
        )

        movie = Movie(
            **movie_in.model_dump(),
        )

        self.assertEqual(
            movie_in.slug,
            movie.slug,
        )
        self.assertEqual(
            movie_in.description,
            movie.description,
        )
        self.assertEqual(
            movie_in.title,
            movie.title,
        )
        self.assertEqual(
            movie_in.year,
            movie.year,
        )
        self.assertEqual(
            movie_in.genre,
            movie.genre,
        )

    def test_movie_create_accepts_different_titles(self) -> None:
        titles = [
            "The Shawshank Redemption",
            "The Godfather",
            "Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb",
            (
                "Borat: Cultural Learnings of America for "
                "Make Benefit Glorious Nation of Kazakhstan"
            ),
            "The Dark Knight",
            "Pulp Fiction",
            "Forrest Gump",
        ]

        for title in titles:
            with self.subTest(title=title, msg=f"test-title-{title}"):
                movie_create = MovieCreate(
                    slug="some-slug",
                    description="Some description",
                    title=title,
                    year=2025,
                    genre="Some genre",
                )
                self.assertEqual(
                    title,
                    movie_create.title,
                )


class MovieUpdateTestCase(TestCase):
    def test_movie_can_be_updated_from_update_schema(self) -> None:
        movie = Movie(
            slug="some-slug",
            description="Some description",
            title="Some title",
            year=2025,
            genre="Some genre",
        )

        movie_in = MovieUpdate(
            title="New title",
            description="New some description",
            year=2026,
            genre="New some genre",
        )

        for field_name, value in movie_in.model_dump().items():
            setattr(movie, field_name, value)

        self.assertEqual(movie_in.title, movie.title)
        self.assertEqual(movie_in.description, movie.description)
        self.assertEqual(movie_in.year, movie.year)
        self.assertEqual(movie_in.genre, movie.genre)

    def test_movie_can_be_partially_updated_from_partial_update_schema(self) -> None:
        movie = Movie(
            slug="some-slug",
            title="Some title",
            description="Some description that is long enough",
            year=2025,
            genre="Some genre",
        )

        movie_in = MoviePartialUpdate(
            description="New some description that is long enough",
        )

        for field_name, value in movie_in.model_dump(exclude_unset=True).items():
            setattr(movie, field_name, value)

        self.assertEqual(movie_in.description, movie.description)
