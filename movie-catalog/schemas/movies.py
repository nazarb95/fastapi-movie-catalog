from pydantic import BaseModel


class MovieBase(BaseModel):
    id: int
    title: str
    description: str
    year: int
    genre: str


class Movie(MovieBase):
    """
    Movie Model
    """

    pass
