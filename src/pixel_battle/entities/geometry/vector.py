from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class Vector:
    x: int = 0
    y: int = 0

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(x=self.x - other.x, y=self.y - other.y)
