from pydantic import BaseModel

from schemas.movies import Movie, MovieCreate

MOVIES = []


class MovieStorage(BaseModel):
    slug_movie: dict[str, Movie] = {}

    def get(self) -> list[Movie]:
        return list(self.slug_movie.values())

    def get_by_slug(self, slug: str) -> Movie | None:
        return self.slug_movie.get(slug)

    def create(self, movie_in: MovieCreate) -> Movie:
        movie = Movie(
            **movie_in.model_dump(),
        )
        self.slug_movie[movie.slug] = movie
        return movie


storage = MovieStorage()

storage.create(
    MovieCreate(
        slug="how-to-train-your-dragon",
        title="How to Train Your Dragon",
        description="A hapless young Viking who aspires to hunt dragons becomes the unlikely friend of a young dragon himself, and learns there may be more to the creatures than he assumed.",
        year=2010,
        genre="Fantasy",
    )
)

storage.create(
    MovieCreate(
        slug="mission-impossible-the-final-reckoning",
        title="Mission: Impossible – The Final Reckoning",
        description="Our lives are the sum of our choices. Tom Cruise is Ethan Hunt in Mission: Impossible — The Final Reckoning.",
        year=2025,
        genre="Thriller",
    )
)
storage.create(
    MovieCreate(
        slug="harry-potter-and-the-sorcerer_s-stone",
        title="Harry Potter and the Sorcerer’s Stone",
        description="An orphaned boy enrolls in a school of wizardry, where he learns the truth about himself, his family and the terrible evil that haunts the magical world.",
        year=2001,
        genre="Fantasy",
    )
)
