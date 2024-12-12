from dataclasses import dataclass

from pixel_battle.entities.quantities.position import Position


@dataclass(kw_only=True, frozen=True, slots=True)
class Rectangle:
    position1: Position
    position2: Position

    @property
    def x_range(self) -> range:
        min_x, max_x = sorted([self.position1.x, self.position2.x])

        return range(min_x, max_x + 1)

    @property
    def y_range(self) -> range:
        min_y, max_y = sorted([self.position1.y, self.position2.y])

        return range(min_y, max_y + 1)

    def __contains__(self, position: Position) -> bool:
        return position.x in self.x_range and position.y in self.y_range
