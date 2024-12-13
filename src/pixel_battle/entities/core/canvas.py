from dataclasses import dataclass

from pixel_battle.entities.quantities.position import Position
from pixel_battle.entities.quantities.rectangle import Rectangle


@dataclass(kw_only=True, frozen=True, slots=True)
class Canvas:
    area: Rectangle


canvas = Canvas(
    area=Rectangle(
        position1=Position(x=0, y=0), position2=Position(x=1000, y=1000)
    )
)
