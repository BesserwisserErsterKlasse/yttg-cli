from re import compile, Pattern
from typing import Final

STARTING_UNDERSCORES: Final[Pattern[str]] = compile(r'^_*')


def to_dash_case(string: str) -> str:
    """Convert a string from PascalCase to dash-case."""

    starting_underscores: str = (
        underscores.group()
        if (underscores := STARTING_UNDERSCORES.match(string)) is not None
        else str()
    )
    return f'{starting_underscores}{(
        str().join(
            symbol if symbol.islower() else f'-{symbol.lower()}' for symbol in string
        ).lstrip('-')
    )}'
