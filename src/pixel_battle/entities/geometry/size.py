from dataclasses import dataclass

from pixel_battle.entities.geometry.vector import Vector


class SizeError(Exception): ...


class NegativeSizeValuesError(SizeError): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Size:
    width: int
    height: int

    def to_vector(self) -> Vector:
        return Vector(x=self.width, y=self.height)

    def to_number_set_vector(self) -> Vector:
        return Vector(x=self.width - 1, y=self.height - 1)

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise NegativeSizeValuesError
