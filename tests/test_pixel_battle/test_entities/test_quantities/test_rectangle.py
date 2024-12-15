from pytest import mark

from pixel_battle.entities.quantities.rectangle import Rectangle, rectangle_with
from pixel_battle.entities.quantities.size import Size
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


@mark.parametrize(
    "min_x_min_y_position, rectangle",
    (
        [
            Vector(x=0, y=0),
            Rectangle(
                position1=Vector(x=0, y=0),
                position2=Vector(x=0, y=0),
            ),
        ],
        [
            Vector(x=-150, y=150),
            Rectangle(
                position1=Vector(x=-150, y=150),
                position2=Vector(x=600, y=200),
            ),
        ],
        [
            Vector(x=-150, y=150),
            Rectangle(
                position1=Vector(x=600, y=200),
                position2=Vector(x=-150, y=150),
            ),
        ],
    )
)
def test_min_x_min_y_position(
    min_x_min_y_position: Vector, rectangle: Rectangle
) -> None:
    assert rectangle.min_x_min_y_position == min_x_min_y_position


@mark.parametrize(
    "max_x_max_y_position, rectangle",
    (
        [
            Vector(x=0, y=0),
            Rectangle(
                position1=Vector(x=0, y=0),
                position2=Vector(x=0, y=0),
            ),
        ],
        [
            Vector(x=600, y=200),
            Rectangle(
                position1=Vector(x=-150, y=150),
                position2=Vector(x=600, y=200),
            ),
        ],
        [
            Vector(x=600, y=200),
            Rectangle(
                position1=Vector(x=600, y=200),
                position2=Vector(x=-150, y=150),
            ),
        ],
    )
)
def test_max_x_max_y_position(
    max_x_max_y_position: Vector, rectangle: Rectangle
) -> None:
    assert rectangle.max_x_max_y_position == max_x_max_y_position


@mark.parametrize(
    "min_x_min_y_position, size, excepted_rectangle",
    (
        [
            Vector(x=0, y=0),
            Size(width=100, height=100),
            Rectangle(
                position1=Vector(x=0, y=0),
                position2=Vector(x=99, y=99),
            ),
        ],
        [
            Vector(x=-100, y=-100),
            Size(width=100, height=100),
            Rectangle(
                position1=Vector(x=-100, y=-100),
                position2=Vector(x=-1, y=-1),
            ),
        ],
        [
            Vector(x=100, y=100),
            Size(width=1, height=100),
            Rectangle(
                position1=Vector(x=100, y=100),
                position2=Vector(x=100, y=199),
            ),
        ],
        [
            Vector(x=-100, y=-100),
            Size(width=1, height=100),
            Rectangle(
                position1=Vector(x=-100, y=-100),
                position2=Vector(x=-100, y=-1),
            ),
        ],
    )
)
def test_rectangle_with(
    min_x_min_y_position: Vector,
    size: Size,
    excepted_rectangle: Rectangle,
) -> None:
    rectangle = rectangle_with(
        size=size, min_x_min_y_position=min_x_min_y_position
    )

    assert rectangle == excepted_rectangle
