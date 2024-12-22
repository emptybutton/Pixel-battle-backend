from pixel_battle.entities.core.chunk import Chunk


def chunk_key_of(chunk: Chunk) -> bytes:
    return bytes([ord("{"), chunk.number.x * 10 + chunk.number.y, ord("}")])