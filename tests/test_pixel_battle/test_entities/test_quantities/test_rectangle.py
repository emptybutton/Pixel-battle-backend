from pytest import mark

from pixel_battle.entities.quantities.rectangle import Rectangle
from pixel_battle.entities.quantities.vector import Vector


@mark.parametrize(
    "position, rectangle",
    (
        [
            Vector(x=0, y=0),
            Rectangle(
                position1=Vector(x=0, y=0),
                position2=Vector(x=0, y=0),
            ),
        ],
        [
            Vector(x=100, y=10),
            Rectangle(
                position1=Vector(x=0, y=0),
                position2=Vector(x=600, y=600),
            ),
        ],
        [
            Vector(x=600, y=600),
            Rectangle(
                position1=Vector(x=0, y=0),
                position2=Vector(x=600, y=600),
            ),
        ],
        [
            Vector(x=600, y=600),
            Rectangle(
                position1=Vector(x=600, y=600),
                position2=Vector(x=0, y=0),
            ),
        ],
    )
)
def test_contains_true(position: Vector, rectangle: Rectangle) -> None:
    assert position in rectangle


@mark.parametrize(
    "position, rectangle",
    (
        [
            Vector(x=1, y=0),
            Rectangle(
                position1=Vector(x=0, y=0),
                position2=Vector(x=0, y=0),
            ),
        ],
        [
            Vector(x=100, y=-10),
            Rectangle(
                position1=Vector(x=0, y=0),
                position2=Vector(x=600, y=600),
            ),
        ],
        [
            Vector(x=600, y=601),
            Rectangle(
                position1=Vector(x=0, y=0),
                position2=Vector(x=600, y=600),
            ),
        ],
    )
)
def test_contains_false(position: Vector, rectangle: Rectangle) -> None:
    assert position not in rectangle
