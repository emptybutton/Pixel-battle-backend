from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from io import BytesIO
from types import TracebackType
from typing import ClassVar

from PIL.Image import Image, frombytes, new

from pixel_battle.application.ports.chunk_view import (
    ChunkView,
    DefaultChunkViewWhen,
)
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.geometry.vector import Vector
from pixel_battle.entities.space.color import RGBColor
from pixel_battle.infrastructure.pillow.types import (
    PillowPixelData,
    PillowPNGImageData,
)


@dataclass(init=False)
class CollectionChunkView(ChunkView):
    _pixel_by_position: dict[Vector, Pixel[RGBColor]]

    def __init__(self, pixels: Iterable[Pixel[RGBColor]] = tuple()) -> None:
        self._pixel_by_position = {pixel.position: pixel for pixel in pixels}

    def __iter__(self) -> Iterator[Pixel[RGBColor]]:
        return iter(self._pixel_by_position.values())

    def __contains__(self, pixel: Pixel[RGBColor]) -> bool:
        return pixel in tuple(iter(self))

    def __len__(self) -> int:
        return len(self._pixel_by_position)

    def __bool__(self) -> bool:
        return bool(self._pixel_by_position)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        pass

    async def redraw_by_pixels(self, pixels: Iterable[Pixel[RGBColor]]) -> None:
        for pixel in pixels:
            self._pixel_by_position[pixel.position] = pixel


class DefaultCollectionChunkViewWhen(
    DefaultChunkViewWhen[CollectionChunkView]
):
    async def __call__(self, *, chunk: Chunk) -> CollectionChunkView:  # noqa: ARG002
        return CollectionChunkView()


class InvalidPNGImageChunkViewModeError(Exception):
    def __init__(self, mode: str) -> None:
        super().__init__(mode)


class InvalidPNGImageChunkViewSizeError(Exception):
    def __init__(self, size: tuple[int, int]) -> None:
        super().__init__(size)


@dataclass(frozen=True, slots=True, eq=False, unsafe_hash=False)
class PNGImageChunkView(ChunkView):  # noqa: PLW1641
    _image: Image
    _mode: ClassVar = "RGB"

    @classmethod
    def _image_size(cls) -> tuple[int, int]:
        size_vector = Chunk.size.to_number_set_vector()

        return (size_vector.x, size_vector.y)

    def __post_init__(self) -> None:
        if self._image.mode != self._mode:
            raise InvalidPNGImageChunkViewModeError(self._image.mode)

        if self._image.size != PNGImageChunkView._image_size():
            raise InvalidPNGImageChunkViewSizeError(self._image.size)

    @classmethod
    def from_pixel_data(
        cls, pixel_data: PillowPixelData
    ) -> "PNGImageChunkView":
        image = frombytes(
            data=pixel_data, mode=cls._mode, size=cls._image_size()
        )

        return PNGImageChunkView(image)

    @classmethod
    def create_default(cls) -> "PNGImageChunkView":
        image = new(
            mode=cls._mode,
            size=PNGImageChunkView._image_size(),
            color=(255, 255, 255),
        )

        return PNGImageChunkView(image)

    def to_pixel_data(self) -> PillowPixelData:
        return self._image.tobytes()

    def to_png_image_data(self) -> PillowPNGImageData:
        with BytesIO() as stream:
            self._image.save(stream, format="png")
            stream.seek(0)
            return stream.read()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PNGImageChunkView):
            return False

        return self._image.tobytes() == other._image.tobytes()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.__close()

    async def redraw_by_pixels(self, pixels: Iterable[Pixel[RGBColor]]) -> None:
        for pixel in pixels:
            coordinates = self.__coordinates_of(pixel)
            value = self.__value_of(pixel)

            self._image.putpixel(coordinates, value)

    def __close(self) -> None:
        self._image.close()

    def __coordinates_of(self, pixel: Pixel[RGBColor]) -> tuple[int, int]:
        position = pixel.position_within_chunk

        return (position.x, position.y)

    def __value_of(self, pixel: Pixel[RGBColor]) -> tuple[int, int, int]:
        return (
            pixel.color.red_value.number,
            pixel.color.green_value.number,
            pixel.color.blue_value.number,
        )


class DefaultPNGImageChunkViewWhen(DefaultChunkViewWhen[PNGImageChunkView]):
    async def __call__(self, *, chunk: Chunk) -> PNGImageChunkView:  # noqa: ARG002
        return PNGImageChunkView.create_default()
