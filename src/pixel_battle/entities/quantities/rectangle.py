from dataclasses import dataclass

from pixel_battle.entities.quantities.vector import Vector


@dataclass(kw_only=True, frozen=True, slots=True)
class Rectangle:
    position1: Vector
    position2: Vector

    @property
    def left_top_position(self) -> Vector:
        return Vector(x=self.x_range.start, y=self.y_range.start)

    @property
    def right_top_position(self) -> Vector:
        return Vector(x=self.x_range.stop - 1, y=self.y_range.start)

    @property
    def left_bottom_position(self) -> Vector:
        return Vector(x=self.x_range.start, y=self.y_range.stop - 1)

    @property
    def right_bottom_position(self) -> Vector:
        return Vector(x=self.x_range.stop - 1, y=self.y_range.stop - 1)

    @property
    def x_range(self) -> range:
        min_x, max_x = sorted([self.position1.x, self.position2.x])

        return range(min_x, max_x + 1)

    @property
    def y_range(self) -> range:
        min_y, max_y = sorted([self.position1.y, self.position2.y])

        return range(min_y, max_y + 1)

    def __contains__(self, position: Vector) -> bool:
        return position.x in self.x_range and position.y in self.y_range
