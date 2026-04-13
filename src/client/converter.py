from uuid import UUID

from cattrs import Converter

converter: Converter = Converter()


@converter.register_structure_hook
def uuid_structure_hook(value: object, _: type[UUID]) -> UUID:
    if isinstance(value, UUID):
        return value
    if isinstance(value, str):
        return UUID(value)
    raise ValueError(f'Cannot construct UUID from {value!r}')


@converter.register_unstructure_hook
def uuid_unstructure_uhook(value: UUID) -> str:
    return str(value)
