from fastapi import (
    FastAPI,
    Request,
)

from schemas.movies import Movie

app = FastAPI(
    title="Movie Catalog",
)


MOVIES = [
    Movie(
        id=1,
        title="How to Train Your Dragon",
        description="A hapless young Viking who aspires to hunt dragons becomes the unlikely friend of a young dragon himself, and learns there may be more to the creatures than he assumed.",
        year=2010,
        genre="Fantasy",
    ),
    Movie(
        id=2,
        title="Mission: Impossible – The Final Reckoning",
        description="Our lives are the sum of our choices. Tom Cruise is Ethan Hunt in Mission: Impossible — The Final Reckoning.",
        year=2025,
        genre="Thriller",
    ),
    Movie(
        id=3,
        title="Harry Potter and the Sorcerer’s Stone",
        description="An orphaned boy enrolls in a school of wizardry, where he learns the truth about himself, his family and the terrible evil that haunts the magical world.",
        year=2001,
        genre="Fantasy",
    ),
]


@app.get("/")
def read_root(
    request: Request,
    name: str = "World",
):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )
    return {
        "message": f"Hello {name}!",
        "docs": str(docs_url),
    }


@app.get(
    "/movies/",
    response_model=list[Movie],
)
def read_movies_list():
    return MOVIES


@app.get(
    "/movies/{movie_id}",
    response_model=Movie,
)
def read_movie(
    movie_id: int,
):
    movie_item = next((movie for movie in MOVIES if movie.id == movie_id), None)
    return movie_item
