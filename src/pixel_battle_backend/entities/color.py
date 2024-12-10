from dataclasses import dataclass


class ColorValueError(Exception): ...


class ColorValueNumberInInvalidRangeError(ColorValueError): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class ColorValue:
    number: int

    def __post_init__(self) -> None:
        if 0 <= self.number <= 255:
            return

        raise ColorValueNumberInInvalidRangeError


@dataclass(kw_only=True, frozen=True, slots=True)
class Color:
    red: ColorValue
    green: ColorValue
    blue: ColorValue


white = Color(
    red=ColorValue(number=0),
    green=ColorValue(number=0),
    blue=ColorValue(number=0),
)


def color_with(
    *,
    red_value_number: int,
    green_value_number: int,
    blue_value_number: int,
) -> Color:
    red = ColorValue(number=red_value_number)
    green = ColorValue(number=green_value_number)
    blue = ColorValue(number=blue_value_number)

    return Color(red=red, green=green, blue=blue)
