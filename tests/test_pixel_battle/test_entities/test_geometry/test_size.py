from pytest import raises

from pixel_battle.entities.geometry.size import NegativeSizeValuesError, Size
from pixel_battle.entities.geometry.vector import Vector


def test_to_vector() -> None:
    vector = Size(width=100, height=100).to_vector()

    assert vector == Vector(x=100, y=100)


def test_negative_size() -> None:
    with raises(NegativeSizeValuesError):
        Size(width=-1, height=10)


def test_zero_size() -> None:
    with raises(NegativeSizeValuesError):
        Size(width=0, height=10)
