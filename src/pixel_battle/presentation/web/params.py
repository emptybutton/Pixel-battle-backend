from typing import Annotated

from pydantic import Field


ChunkNumberX = Annotated[
    int, Field(alias="chunkNumberX", ge=0, lt=10)
]

ChunkNumberY = Annotated[
    int, Field(alias="chunkNumberY", ge=0, lt=10)
]
