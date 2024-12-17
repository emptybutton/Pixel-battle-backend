from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from pixel_battle.application.ports.chunk_view import ChunkView
from pixel_battle.application.ports.pixels import Pixels
from pixel_battle.application.ports.users import Users
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel, recolored_by
from pixel_battle.entities.core.user import User, new_user_when
from pixel_battle.entities.quantities.color import (
    RGBColor,
    RGBColorValue,
    unknown_color,
)
from pixel_battle.entities.quantities.time import Time
from pixel_battle.entities.quantities.vector import Vector


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    user: User
    pixel: Pixel[RGBColor] | None


@dataclass(kw_only=True, frozen=True, slots=True)
class RecolorPixel[ChunkViewT: ChunkView]:
    users: Users
    pixel_batch: Pixels

    async def __call__(
        self,
        user_id: UUID | None,
        pixel_position_x: int,
        pixel_position_y: int,
        chunk_number_x: int,
        chunk_number_y: int,
        new_color_red_value_number: int,
        new_color_green_value_number: int,
        new_color_blue_value_number: int,
    ) -> Output:
        current_time = Time(datetime=datetime.now(UTC))

        if user_id is not None:
            user = await self.users.user_with_id(user_id)
        else:
            user = None

        if user is None:
            user = new_user_when(current_time=current_time)
            return Output(user=user, pixel=None)

        chunk = Chunk(number=ChunkNumber(x=chunk_number_x, y=chunk_number_y))

        pixel_position = Vector(x=pixel_position_x, y=pixel_position_y)
        pixel = Pixel(position=pixel_position, color=unknown_color)

        new_pixel_color = RGBColor(
            red=RGBColorValue(number=new_color_red_value_number),
            green=RGBColorValue(number=new_color_green_value_number),
            blue=RGBColorValue(number=new_color_blue_value_number),
        )

        result = recolored_by(
            user,
            pixel,
            new_color=new_pixel_color,
            current_time=current_time,
            chunk=chunk,
        )

        await self.users.put(result.user)
        await self.pixel_batch.add(result.pixel)

        return Output(user=result.user, pixel=result.pixel)
