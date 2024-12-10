from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class Position:
    x: int
    y: int
