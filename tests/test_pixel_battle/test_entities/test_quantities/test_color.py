from pytest import raises

from pixel_battle.entities.quantities.color import (
    RGBColorValue,
    RGBColorValueNumberInInvalidRangeError,
)


def test_negative_rgb_color_value() -> None:
    with raises(RGBColorValueNumberInInvalidRangeError):
        RGBColorValue(number=-1)


def test_too_large_rgb_color_value() -> None:
    with raises(RGBColorValueNumberInInvalidRangeError):
        RGBColorValue(number=256)
