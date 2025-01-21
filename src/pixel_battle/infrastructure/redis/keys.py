from pixel_battle.entities.core.chunk import Chunk
from pixel_battle.infrastructure.encoding import encoded_chunk_when


def chunk_key_when(*, chunk: Chunk) -> bytes:
    encoded_chunk = encoded_chunk_when(chunk=chunk)

    return b"{" + encoded_chunk + b"}"
