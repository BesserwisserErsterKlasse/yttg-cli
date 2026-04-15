from re import compile, Match, Pattern, RegexFlag
from typing import Final

from cattrs import structure

from client.types import YttgCommand, YttgRequest

COMMAND: Final[Pattern[str]] = compile(
    r'''
    --[a-zA-Z][a-zA-Z0-9\-_]*=[^\s\"]*
    |--[a-zA-Z][a-zA-Z0-9\-_]*=\"[^\n\"]*\"
    |[^\s\"]+
    |\"[^\n\"]*\"
    ''',
    flags=RegexFlag.VERBOSE,
)
KEYWORD: Final[Pattern[str]] = compile(r'--(?P<name>[a-zA-Z0-9_-]+)=(?P<value>[^\s]+)')
REMOVE_QUOTES_SLICE: Final[slice] = slice(1, -1, None)
WHOLE_STRING_SLICE: Final[slice] = slice(None, None, None)


def remove_quotes(argument: str) -> str:
    """Remove surrounding quotes."""

    if argument.startswith('\"') and argument.endswith('\"'):
        return argument[REMOVE_QUOTES_SLICE]
    if argument.startswith('--') and '=' in argument:
        name, value = argument.split(sep='=', maxsplit=1)
        return f'{name}={(
            value[
                REMOVE_QUOTES_SLICE
                if value.startswith('\"') and value.endswith('\"')
                else WHOLE_STRING_SLICE
            ]
        )}'
    return argument


def parse_arguments(arguments: list[str], argument_order: list[str]) -> dict[str, str]:
    """Parse positional and keyword arguments."""

    result: dict[str, str] = {}
    for argument, field_name in zip(arguments, argument_order):
        if argument.startswith('--'):
            break
        result[field_name] = argument
    keywords_slice: slice = slice(len(result), None)
    for keyword in arguments[keywords_slice]:
        m: Match[str] | None = KEYWORD.match(keyword)
        if m is None:
            raise ValueError(f'Invalid keyword argument: \"{keyword}\"')
        if m.group('name') not in argument_order:
            raise ValueError(f'Unknown keyword argument: \"{m.group('name')}\"')
        result[m.group('name')] = m.group('value')
    return result


def parse_command(command: str) -> YttgRequest:
    """Parse a given CLI command into YttgRequest object."""

    command_name, *arguments = map(remove_quotes, COMMAND.findall(string=command))
    request_type: type[YttgRequest] = YttgRequest.get_factory(YttgCommand(command_name))
    return structure(
        obj=parse_arguments(arguments, request_type.argument_order),
        cl=request_type,
    )
