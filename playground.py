from typing import Annotated, get_type_hints


def QueryParameterConstrainsts(min_length: int = 0, max_length: int = 100):
    return {"min_length": min_length, "max_length": max_length}


def my_function(value: Annotated[str, QueryParameterConstrainsts(12, 200)]):
    print(value)


my_function("Hello")

hints = get_type_hints(my_function, include_extras=True)
print(hints["value"].__metadata__)
