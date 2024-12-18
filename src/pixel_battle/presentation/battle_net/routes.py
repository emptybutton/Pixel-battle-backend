from asyncio import gather
from itertools import chain
from typing import Literal
from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, WebSocket
from pydantic import BaseModel, Field, ValidationError

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.application.ports.chunk_view import ChunkView
from pixel_battle.entities.core.pixel import (
    DifferentChunkToRecolorError,
    PixelOutOfCanvasError,
    UserHasNoRightToRecolorError,
)
from pixel_battle.entities.quantities.color import (
    RGBColorValueNumberInInvalidRangeError,
)
from pixel_battle.entities.quantities.time import NotUTCTimeError
from pixel_battle.presentation.battle_net.ws import (
    ConnectionGroupByGroupID,
    texts_and_then_disconnect_of,
)


router = APIRouter()


class ErrorSchema(BaseModel):
    type: str


class ErrorListSchema(BaseModel):
    error_models: list[BaseModel] = Field(alias="errors")

    @classmethod
    def from_(cls, error: ValidationError) -> "ErrorListSchema":
        error_models: list[BaseModel] = [
            ErrorSchema(type=raw_error["type"]) for raw_error in error.errors()
        ]

        return ErrorListSchema(errors=error_models)


class RecolorPixelSchema(BaseModel):
    user_id: UUID | None = Field(alias="userID")
    pixel_position: tuple[int, int] = Field(alias="pixelPosition")
    new_pixel_color: tuple[int, int, int] = Field(alias="newPixelColor")


class RegistrationSchema(BaseModel):
    user_id: UUID


class RecoloredPixelSchema(BaseModel):
    pixel_position: tuple[int, int] | None = Field(alias="pixelPosition")
    new_pixel_color: tuple[int, int, int] | None = Field(alias="newPixelColor")


class NotRecoloredPixelSchema(BaseModel):
    type: Literal[
        "pixelOutOfCanvas",
        "noRight",
        "differentChunk",
        "invalidColorValueRange",
        "notUTCDatetimeOfUserObtainingRecoloringRight",
    ]


@router.websocket("/chunk/{chunk_number_x}/{chunk_number_y}")
@inject
async def chunk_channel(
    current_connection: WebSocket,
    connection_group_by_group_id: FromDishka[ConnectionGroupByGroupID],
    recolor_pixel: FromDishka[RecolorPixel[ChunkView]],
    chunk_number_x: int,
    chunk_number_y: int,
) -> None:
    await current_connection.accept()

    group_id = (chunk_number_x, chunk_number_y)
    current_connection_group = connection_group_by_group_id[group_id]
    current_connection_group.add(current_connection)

    output_model: BaseModel

    jsons = texts_and_then_disconnect_of(
        current_connection, its_group=current_connection_group
    )
    async for json in jsons:
        try:
            input_model = RecolorPixelSchema.model_validate_json(json)
        except ValidationError as error:
            output_model = ErrorListSchema.from_(error)
            await current_connection.send_text(output_model.model_dump_json())
            continue

        error_output_model: BaseModel | None = None

        try:
            result = await recolor_pixel(
                user_id=input_model.user_id,
                pixel_position_x=input_model.pixel_position[0],
                pixel_position_y=input_model.pixel_position[1],
                chunk_number_x=chunk_number_x,
                chunk_number_y=chunk_number_y,
                new_color_red_value_number=input_model.new_pixel_color[0],
                new_color_green_value_number=input_model.new_pixel_color[1],
                new_color_blue_value_number=input_model.new_pixel_color[2],
            )
        except PixelOutOfCanvasError:
            error_output_model = NotRecoloredPixelSchema(
                type="pixelOutOfCanvas"
            )
        except UserHasNoRightToRecolorError:
            error_output_model = NotRecoloredPixelSchema(type="noRight")
        except DifferentChunkToRecolorError:
            error_output_model = NotRecoloredPixelSchema(type="differentChunk")
        except RGBColorValueNumberInInvalidRangeError:
            error_output_model = NotRecoloredPixelSchema(
                type="invalidColorValueRange"
            )
        except NotUTCTimeError:
            error_output_model = NotRecoloredPixelSchema(
                type="notUTCDatetimeOfUserObtainingRecoloringRight"
            )

        if error_output_model is not None:
            output_model = ErrorListSchema(errors=[error_output_model])
            await current_connection.send_text(output_model.model_dump_json())
            continue

        if result.pixel is None:
            output_model = RegistrationSchema(user_id=result.user.id)
            await current_connection.send_text(output_model.model_dump_json())
            continue

        pixel_position = (result.pixel.position.x, result.pixel.position.y)
        pixel_color = (
            result.pixel.color.red.number,
            result.pixel.color.green.number,
            result.pixel.color.blue.number,
        )
        output_model = RecoloredPixelSchema(
            pixelPosition=pixel_position,
            newPixelColor=pixel_color,
        )
        output = output_model.model_dump_json()

        await gather(*(
            connection.send_text(output)
            for connection in chain.from_iterable(
                connection_group_by_group_id.values()
            )
        ))
