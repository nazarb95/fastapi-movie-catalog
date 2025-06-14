import logging
from os import getenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MOVIE_STORAGE_FILE_PATH = BASE_DIR / "movies.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

# Only for demo!
# no real users in code!!
USERS_DB: dict[str, str] = {
    # username: password
    "nazar": "qwerty",
    "anton": "password",
}


REDIS_HOST = "localhost"
REDIS_PORT = int(getenv("REDIS_PORT", 0)) or 6379  # noqa: PLW1508
REDIS_DB = 0
REDIS_DB_TOKENS = 1
REDIS_DB_USERS = 2
REDIS_DB_MOVIES = 3

REDIS_TOKENS_SET_NAME = "tokens"
REDIS_MOVIE_HASH_HAME = "movies"
