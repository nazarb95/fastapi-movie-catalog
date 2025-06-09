from os import getenv

if getenv("TESTING") != "1":
    raise OSError(  # noqa: TRY003
        "Environment is not ready for testing",  # noqa: EM101
    )


def total(a: int, b: int) -> int:
    return a + b
