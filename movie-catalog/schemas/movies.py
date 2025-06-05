from typing import Annotated

from annotated_types import Len, Ge, Le
from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    description: str
    year: int
    genre: str


class MovieCreate(MovieBase):
    """
    Model for movie creation
    """

    title: Annotated[str, Len(min_length=1, max_length=70)]
    description: Annotated[str, Len(min_length=10, max_length=250)]
    year: Annotated[int, Ge(1900), Le(2026)]
    genre: Annotated[str, Len(min_length=1, max_length=25)]


class Movie(MovieBase):
    """
    Movie Model
    """

    id: int

    pass
