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
    red: RGBColorValue
    green: RGBColorValue
    blue: RGBColorValue


@dataclass(kw_only=True, frozen=True, slots=True)
class UndefinedColor(Color): ...


undefined_color = UndefinedColor()

white = RGBColor(
    red=RGBColorValue(number=0),
    green=RGBColorValue(number=0),
    blue=RGBColorValue(number=0),
)
