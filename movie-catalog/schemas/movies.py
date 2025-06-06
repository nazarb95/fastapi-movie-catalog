from typing import Annotated

from annotated_types import Len, Ge, Le
from pydantic import BaseModel


TitleString = Annotated[
    str,
    Len(min_length=1, max_length=70),
]
SlugString = Annotated[
    str,
    Len(min_length=1, max_length=70),
]
DescriptionString = Annotated[
    str,
    Len(min_length=10, max_length=250),
]
YearInt = Annotated[
    int,
    Ge(1900),
    Le(2026),
]
GenreString = Annotated[
    str,
    Len(min_length=1, max_length=25),
]


class MovieBase(BaseModel):

    title: str
    description: DescriptionString = ""
    year: YearInt
    genre: GenreString


class MovieCreate(MovieBase):
    """
    Model for movie creation
    """

    slug: SlugString
    title: TitleString
    year: YearInt
    genre: GenreString


class MovieUpdate(MovieBase):
    """
    Model for updating movie information
    """

    description: DescriptionString


class MoviePartialUpdate(MovieBase):
    """
    Model for partial updating movie information
    """

    title: TitleString | None = None
    description: DescriptionString | None = None
    year: YearInt | None = None
    genre: GenreString | None = None


class MovieRead(MovieBase):
    """
    Model for reading data
    """

    slug: str


class Movie(MovieBase):
    """
    Movie Model
    """

    slug: str
    notes: str = "This movie is really cool"
