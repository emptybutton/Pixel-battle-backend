from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from itertools import flatten
from operator import add
from typing import Iterable, Iterator, Sequence

from redis.asyncio.cluster import RedisCluster

from pixel_battle.application.ports.pixels import Pixels
from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.entities.core.pixel import Pixel
from pixel_battle.entities.quantities.color import RGBColor, RGBColorValue
from pixel_battle.entities.quantities.vector import Vector


@dataclass(init=False)
class InMemoryPixels(Pixels):
    __pixels_by_chunk: defaultdict[Chunk, list[Pixel[RGBColor]]]

    def __init__(self, pixels: Iterable[Pixel[RGBColor]]) -> None:
        self.__pixels_by_chunk = defaultdict()

        for pixel in pixels:
            self.__pixels_by_chunk[pixel.chunk].append(pixel)

    def __iter__(self) -> Iterator[Pixel[RGBColor]]:
        return iter(flatten(self.__pixels_by_chunk.values()))

    def __len__(self) -> int:
        return reduce(add, map(len, self.__pixels_by_chunk.values()))

    def __bool__(self) -> bool:
        return any(map(bool, self.__pixels_by_chunk.values()))

    async def add(self, pixel: Pixel[RGBColor]) -> None:
        self.__pixels_by_chunk[pixel.chunk].append(pixel)

    async def pixels_of_chunk(self, chunk: Chunk) -> Sequence[Pixel[RGBColor]]:
        return tuple(self.__pixels_by_chunk[chunk])

    async def lremove_pixels_of_chunk(
        self, chunk: Chunk, *, amount: int
    ) -> None:
        pixels = self.__pixels_by_chunk[chunk]
        del pixels[:amount]


@dataclass(kw_only=True, frozen=True, slots=True)
class InRedisClusterPixels(Pixels):
    redis_cluster: RedisCluster

    async def add(self, pixel: Pixel[RGBColor]) -> None:
        key = self.__key_by(pixel.chunk)
        value = self.__bytes_of(pixel)

        await self.redis_cluster.rpush(key, value)

    async def pixels_of_chunk(self, chunk: Chunk) -> Sequence[Pixel[RGBColor]]:
        key = self.__key_by(chunk)
        arrays = await self.redis_cluster.lrange(key, 0, -1)

        return tuple(self.__pixel_of(bytes_, chunk=chunk) for bytes_ in arrays)

    async def lremove_pixels_of_chunk(
        self, chunk: Chunk, *, amount: int
    ) -> None:
        key = self.__key_by(chunk)
        await self.redis_cluster.lpop(key, count=amount)

    def __key_by(self, chunk: Chunk) -> str:
        raw_key = bytes([chunk.number.x, chunk.number.y]) + b"pixels"
        return raw_key.decode()

    def __bytes_of(self, pixel: Pixel[RGBColor]) -> bytes:
        return bytes([
            pixel.position_within_chunk.x,
            pixel.position_within_chunk.y,
            pixel.color.red.number,
            pixel.color.green.number,
            pixel.color.blue.number,
        ])

    def __pixel_of(self, bytes_: bytes, *, chunk: Chunk) -> Pixel[RGBColor]:
        position_within_chunk = Vector(x=bytes_[0], y=bytes_[1])
        position = position_within_chunk + chunk.area.min_x_min_y_position

        red = RGBColorValue(number=bytes_[2])
        green = RGBColorValue(number=bytes_[3])
        blue = RGBColorValue(number=bytes_[4])
        color = RGBColor(red=red, green=green, blue=blue)

        return Pixel(position=position, color=color)
