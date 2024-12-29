from dataclasses import dataclass

from pixel_battle.entities.geometry.rectangle import Rectangle, rectangle_with
from pixel_battle.entities.geometry.size import Size
from pixel_battle.entities.geometry.vector import Vector


@dataclass(kw_only=True, frozen=True, slots=True)
class Canvas:
    area: Rectangle


canvas = Canvas(
    area=rectangle_with(
        min_x_min_y_position=Vector(x=0, y=0),
        size=Size(width=1000, height=1000),
    )
)
