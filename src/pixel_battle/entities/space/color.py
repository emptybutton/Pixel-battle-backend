from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class Color: ...


class RGBColorValueError(Exception): ...


class RGBColorValueNumberInInvalidRangeError(RGBColorValueError): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class RGBColorValue:
    number: int

    def __post_init__(self) -> None:
        if 0 <= self.number <= 255:
            return

        raise RGBColorValueNumberInInvalidRangeError


@dataclass(kw_only=True, frozen=True, slots=True)
class RGBColor(Color):
    red_value: RGBColorValue
    green_value: RGBColorValue
    blue_value: RGBColorValue


@dataclass(kw_only=True, frozen=True, slots=True)
class UnknownColor(Color): ...


unknown_color = UnknownColor()

white = RGBColor(
    red_value=RGBColorValue(number=255),
    green_value=RGBColorValue(number=255),
    blue_value=RGBColorValue(number=255),
)

black = RGBColor(
    red_value=RGBColorValue(number=0),
    green_value=RGBColorValue(number=0),
    blue_value=RGBColorValue(number=0),
)

red = RGBColor(
    red_value=RGBColorValue(number=255),
    green_value=RGBColorValue(number=0),
    blue_value=RGBColorValue(number=0),
)

green = RGBColor(
    red_value=RGBColorValue(number=0),
    green_value=RGBColorValue(number=255),
    blue_value=RGBColorValue(number=0),
)

blue = RGBColor(
    red_value=RGBColorValue(number=0),
    green_value=RGBColorValue(number=0),
    blue_value=RGBColorValue(number=255),
)
