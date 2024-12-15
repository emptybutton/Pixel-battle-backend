from pixel_battle.entities.core.chunk import Chunk


def chunk_key_of(chunk: Chunk) -> str:
    return f"{{{chunk.number.x} {chunk.number.y}}}"
