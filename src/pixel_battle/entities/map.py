from dataclasses import dataclass
from functools import cached_property

from pixel_battle.entities.position import Position


@dataclass(kw_only=True, frozen=True, slots=True)
class Rectangle:
    position1: Position
    position2: Position

    @cached_property
    def x_range(self) -> range:
        return range(*sorted([self.position1.x, self.position2.x + 1]))

    @cached_property
    def y_range(self) -> range:
        return range(*sorted([self.position1.y, self.position2.y + 1]))

    def __contains__(self, position: Position) -> bool:
        return position.x in self.x_range and position.y in self.y_range


map_ = Rectangle(
    position1=Position(x=0, y=0),
    position2=Position(x=1600, y=400),
)
