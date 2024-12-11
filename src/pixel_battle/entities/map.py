from dataclasses import dataclass
from functools import cached_property

from pixel_battle.entities.postition import Position


@dataclass(kw_only=True, frozen=True, slots=True)
class Rectangle:
    postition1: Position
    postition2: Position

    @cached_property
    def x_range(self) -> range:
        return range(*sorted([self.postition1.x, self.postition2.x + 1]))

    @cached_property
    def y_range(self) -> range:
        return range(*sorted([self.postition1.y, self.postition2.y + 1]))

    def __contains__(self, postition: Position) -> bool:
        return postition.x in self.x_range and postition.y in self.y_range


map_ = Rectangle(
    position1=Position(x=0, y=0),
    postition2=Position(x=1590, y=400),
)
