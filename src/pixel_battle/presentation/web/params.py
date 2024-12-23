from typing import Annotated

from pydantic import Field


ChunkNumberX = Annotated[
    int, Field(alias="chunkNumberX", min_length=0, max_length=9)
]

ChunkNumberY = Annotated[
    int, Field(alias="chunkNumberY", min_length=0, max_length=9)
]
