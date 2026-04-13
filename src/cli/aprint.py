async def aprint(*values: object, sep: str = ' ', end: str = '\n') -> None:
    """Async version of print."""

    print(*values, sep=sep, end=end)
