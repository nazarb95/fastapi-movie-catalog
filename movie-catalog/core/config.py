import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MOVIE_STORAGE_FILE_PATH = BASE_DIR / "movies.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

# Never store real tokens here!
# Only fake values
API_TOKENS: frozenset[str] = frozenset(
    {
        "Eklut4DnEUMsSUGQfUCXHA",
        "lUs0crT3NJMaB-SZiWxBNg",
    }
)

# Only for demo!
# no real users in code!!
USERS_DB: dict[str, str] = {
    # username: password
    "nazar": "qwerty",
    "anton": "password",
}
