from typing import Iterable, Self

from pydantic import BaseModel, Field

from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor


class ErrorListSchema[ErrorSchemaT](BaseModel):
    error_models: tuple[ErrorSchemaT] = Field(alias="errors")


class ErrorSchema(BaseModel):
    def to_list(self) -> ErrorListSchema[Self]:
        return ErrorListSchema(errors=(self, ))


class RecoloredPixelSchema(BaseModel):
    pixel_position: tuple[int, int] | None = Field(alias="pixelPosition")
    new_pixel_color: tuple[int, int, int] | None = Field(alias="newPixelColor")

    @classmethod
    def of(cls, pixel: Pixel[RGBColor]) -> "RecoloredPixelSchema":
        pixel_position = (pixel.position.x, pixel.position.y)
        new_pixel_color = (
            pixel.color.red.number,
            pixel.color.green.number,
            pixel.color.blue.number,
        )

        return RecoloredPixelSchema(
            pixelPosition=pixel_position, newPixelColor=new_pixel_color
        )


class RecoloredPixelListSchema(BaseModel):
    pixels: list[RecoloredPixelSchema]

    @classmethod
    def of(
        cls, pixels: Iterable[Pixel[RGBColor]]
    ) -> "RecoloredPixelListSchema":
        pixels = list(map(RecoloredPixelSchema.of, pixels))

        return RecoloredPixelListSchema(pixels=pixels)
