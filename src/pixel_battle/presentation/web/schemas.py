from collections.abc import Iterable
from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field

from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.space.color import RGBColor
from pixel_battle.entities.space.time_delta import TimeDelta


class NoDataSchema(BaseModel): ...


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
            pixel.color.red_value.number,
            pixel.color.green_value.number,
            pixel.color.blue_value.number,
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


class TimeDeltaSchema(BaseModel):
    start_time: datetime = Field(alias="startTime")
    end_time: datetime = Field(alias="endTime")

    @classmethod
    def of(cls, time_delta: TimeDelta) -> "TimeDeltaSchema":
        return TimeDeltaSchema(
            startTime=time_delta.start_time.datetime,
            endTime=time_delta.end_time.datetime,
        )
