__all__ = ("app",)

from typing import Annotated

import typer
from rich import print
from rich.markdown import Markdown

from api.api_v1.auth.services import redis_tokens as tokens

app = typer.Typer(
    name="token",
    help="Tokens management.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(help="The token to check"),
    ],
) -> None:
    """
    Check if the passed token is valid - exists or not.
    """
    print(
        f"Token [bold]{token}[/bold]",
        (
            "[bold green]exists.[/bold green]"
            if tokens.token_exists(token)
            else "[bold red]does not exist.[/bold red]"
        ),
    )


@app.command(name="list")
def list_tokens() -> None:
    """
    Get all tokens
    """
    print(Markdown("# Tokens:\n"))
    print(Markdown("\n- ".join([""] + tokens.get_tokens())))
    print()


@app.command()
def create() -> None:
    """
    Create a new token and add it to the database.
    """
    token = tokens.generate_and_save_token()
    print(
        f"Token [bold]{token}[/bold] was [green]created[/green] and saved to the database"
    )


@app.command()
def add(
    token: Annotated[
        str,
        typer.Argument(help="The token to add"),
    ],
) -> None:
    """
    Add a new token to the database.
    """
    tokens.add_token(token)
    print(f"Token [bold]{token}[/bold] was added to the database")


@app.command(name="rm")
def remove(
    token: Annotated[
        str,
        typer.Argument(help="The token to remove"),
    ],
) -> None:
    """
    Remove a token from the database.
    """
    if not tokens.token_exists(token):
        print(f"Token [bold]{token} [red]does not exist[/red][/bold].")
        return
    tokens.delete_token(token)
    print(
        f"Token [bold]{token}[/bold] has been [green]removed[/green] from the database"
    )
