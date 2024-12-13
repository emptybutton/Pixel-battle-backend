from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from pixel_battle.application.ports.chunk_view import (
    ChunkView,
    ChunkViews,
    DefaultChunkViewOf,
)
from pixel_battle.application.ports.transaction import TransactionOf
from pixel_battle.entities.core.chunk import Chunk, ChunkNumber
from pixel_battle.entities.core.pixel import Pixel, recolored_by
from pixel_battle.entities.core.user import User, new_user_when
from pixel_battle.entities.quantities.color import (
    RGBColor,
    RGBColorValue,
    unknown_color,
)
from pixel_battle.entities.quantities.position import Position
from pixel_battle.entities.quantities.time import Time


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    user: User
    pixel: Pixel[RGBColor] | None


@dataclass(kw_only=True, frozen=True, slots=True)
class RecolorPixel[ChunkViewT: ChunkView]:
    chunk_views: ChunkViews[ChunkViewT]
    transaction_of: TransactionOf[ChunkViews[ChunkViewT]]
    default_chunk_view_of: DefaultChunkViewOf[ChunkViewT]

    async def __call__(
        self,
        user_id: UUID | None,
        datetime_of_user_obtaining_recoloring_right: datetime | None,
        pixel_position_x: int,
        pixel_position_y: int,
        chunk_number_x: int,
        chunk_number_y: int,
        new_color_red_value_number: int,
        new_color_green_value_number: int,
        new_color_blue_value_number: int,
    ) -> Output:
        current_time = Time(datetime=datetime.now(UTC))

        user_chunk_number = ChunkNumber(x=chunk_number_x, y=chunk_number_y)
        user_chunk = Chunk(number=user_chunk_number)

        if (
            user_id is None
            or datetime_of_user_obtaining_recoloring_right is None
        ):
            user = new_user_when(current_time=current_time, chunk=user_chunk)
            return Output(user=user, pixel=None)

        user_time = Time(datetime=datetime_of_user_obtaining_recoloring_right)
        user = User(
            id=user_id,
            time_of_obtaining_recoloring_right=user_time,
            chunk=user_chunk,
        )

        pixel_position = Position(x=pixel_position_x, y=pixel_position_y)
        pixel = Pixel(position=pixel_position, color=unknown_color)

        new_pixel_color = RGBColor(
            red=RGBColorValue(number=new_color_red_value_number),
            green=RGBColorValue(number=new_color_green_value_number),
            blue=RGBColorValue(number=new_color_blue_value_number),
        )

        result = recolored_by(
            user, pixel, new_color=new_pixel_color, current_time=current_time
        )

        async with self.transaction_of(self.chunk_views):
            chunk_view = await self.chunk_views.chunk_view_of(
                result.pixel.chunk
            )

            if chunk_view is None:
                chunk_view = await self.default_chunk_view_of(
                    result.pixel.chunk
                )

            await chunk_view.redraw(result.pixel)
            await self.chunk_views.put(chunk_view, chunk=result.pixel.chunk)

            return Output(user=result.user, pixel=result.pixel)
