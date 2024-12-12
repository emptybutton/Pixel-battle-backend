from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class Position:
    x: int
    y: int


zero_position = Position(x=0, y=0)
