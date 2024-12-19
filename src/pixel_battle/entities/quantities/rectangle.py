from dataclasses import dataclass

from pixel_battle.entities.quantities.size import Size
from pixel_battle.entities.quantities.vector import Vector


@dataclass(kw_only=True, frozen=True, slots=True, eq=False)
class Rectangle:
    position1: Vector
    position2: Vector

    @property
    def min_x_min_y_position(self) -> Vector:
        return Vector(x=self.x_range.start, y=self.y_range.start)

    @property
    def max_x_min_y_position(self) -> Vector:
        return Vector(x=self.x_range.stop - 1, y=self.y_range.start)

    @property
    def min_x_max_y_position(self) -> Vector:
        return Vector(x=self.x_range.start, y=self.y_range.stop - 1)

    @property
    def max_x_max_y_position(self) -> Vector:
        return Vector(x=self.x_range.stop - 1, y=self.y_range.stop - 1)

    @property
    def x_range(self) -> range:
        min_x, max_x = sorted([self.position1.x, self.position2.x])

        return range(min_x, max_x + 1)

    @property
    def y_range(self) -> range:
        min_y, max_y = sorted([self.position1.y, self.position2.y])

        return range(min_y, max_y + 1)

    @property
    def size(self) -> Size:
        return Size(width=len(self.x_range), height=len(self.y_range))

    def __contains__(self, position: Vector) -> bool:
        return position.x in self.x_range and position.y in self.y_range

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rectangle):
            return False

        return self.x_range == other.x_range and self.y_range == other.y_range

    def __hash__(self) -> int:
        return hash(type(self)) + hash((self.x_range, self.y_range))


def rectangle_with(*, size: Size, min_x_min_y_position: Vector) -> Rectangle:
    position2_offset = size.to_number_set_vector()

    return Rectangle(
        position1=min_x_min_y_position,
        position2=min_x_min_y_position + position2_offset,
    )
