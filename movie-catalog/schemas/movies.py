from typing import Annotated

from annotated_types import Len, Ge, Le
from pydantic import BaseModel


class MovieBase(BaseModel):

    title: str
    description: Annotated[
        str,
        Len(min_length=10, max_length=250),
    ] = ""
    year: int
    genre: str


class MovieCreate(MovieBase):
    """
    Model for movie creation
    """

    slug: Annotated[
        str,
        Len(min_length=1, max_length=70),
    ]
    title: Annotated[
        str,
        Len(min_length=1, max_length=70),
    ]
    year: Annotated[int, Ge(1900), Le(2026)]
    genre: Annotated[
        str,
        Len(min_length=1, max_length=25),
    ]


class MovieUpdate(MovieBase):
    """
    Model for updating movie information
    """

    description: Annotated[
        str,
        Len(min_length=10, max_length=250),
    ]


class Movie(MovieBase):
    """
    Movie Model
    """

    slug: str
