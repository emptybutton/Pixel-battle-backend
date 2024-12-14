from dataclasses import dataclass

from pixel_battle.entities.quantities.rectangle import Rectangle
from pixel_battle.entities.quantities.vector import Vector


@dataclass(kw_only=True, frozen=True, slots=True)
class Canvas:
    area: Rectangle


canvas = Canvas(
    area=Rectangle(
        position1=Vector(x=0, y=0), position2=Vector(x=1000, y=1000)
    )
)
