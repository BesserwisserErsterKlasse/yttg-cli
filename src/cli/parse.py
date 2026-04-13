from inspect import signature
from re import compile, Match, Pattern
from typing import Final

from cattrs import structure

from client.types import YttgCommand, YttgRequest

KEYWORD: Final[Pattern[str]] = compile(r'--(?P<name>[a-zA-Z0-9_-]+)=(?P<value>[^\s]+)')


def parse_arguments(arguments: list[str], field_names: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for argument, field_name in zip(arguments, field_names):
        if argument.startswith('--'):
            break
        result[field_name] = argument
    keywords_slice: slice = slice(len(result), None)
    for keyword in arguments[keywords_slice]:
        m: Match[str] | None = KEYWORD.match(keyword)
        if m is None:
            raise ValueError(f'Invalid keyword argument \"{keyword}\"')
        if m.group('name') not in field_names:
            raise ValueError(f'Unknown keyword argument \"{m.group('name')}\"')
        result[m.group('name')] = m.group('value')
    return result


def parse_command(command: str) -> YttgRequest:
    """Parse a given CLI command into YttgRequest object."""

    command_name, *original_arguments = command.strip().split(sep=' ')
    request_type: type[YttgRequest] = YttgRequest.get_factory(YttgCommand(command_name))
    return structure(
        obj=parse_arguments(
            arguments=original_arguments,
            field_names=list(signature(request_type.__init__).parameters)[:0:-1],
        ),
        cl=request_type,
    )
