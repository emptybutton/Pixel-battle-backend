from pytest import mark

from pixel_battle.entities.quantities.position import Position
from pixel_battle.entities.quantities.rectangle import Rectangle


@mark.parametrize(
    "position, rectangle",
    (
        [
            Position(x=0, y=0),
            Rectangle(
                position1=Position(x=0, y=0),
                position2=Position(x=0, y=0),
            ),
        ],
        [
            Position(x=100, y=10),
            Rectangle(
                position1=Position(x=0, y=0),
                position2=Position(x=600, y=600),
            ),
        ],
        [
            Position(x=600, y=600),
            Rectangle(
                position1=Position(x=0, y=0),
                position2=Position(x=600, y=600),
            ),
        ],
        [
            Position(x=600, y=600),
            Rectangle(
                position1=Position(x=600, y=600),
                position2=Position(x=0, y=0),
            ),
        ],
    )
)
def test_contains_true(position: Position, rectangle: Rectangle) -> None:
    assert position in rectangle


@mark.parametrize(
    "position, rectangle",
    (
        [
            Position(x=1, y=0),
            Rectangle(
                position1=Position(x=0, y=0),
                position2=Position(x=0, y=0),
            ),
        ],
        [
            Position(x=100, y=-10),
            Rectangle(
                position1=Position(x=0, y=0),
                position2=Position(x=600, y=600),
            ),
        ],
        [
            Position(x=600, y=601),
            Rectangle(
                position1=Position(x=0, y=0),
                position2=Position(x=600, y=600),
            ),
        ],
    )
)
def test_contains_false(position: Position, rectangle: Rectangle) -> None:
    assert position not in rectangle
