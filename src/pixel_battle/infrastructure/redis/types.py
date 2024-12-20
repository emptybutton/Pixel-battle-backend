type RedisStreamKey = bytes
type RedisStreamOffset = bytes

type RedisStreamEventBody = dict[bytes, bytes]
type RedisStreamEvent = tuple[RedisStreamOffset, RedisStreamEventBody]
type RedisStreamEvents = list[RedisStreamEvent]
type RedisStreamResult = tuple[RedisStreamKey, RedisStreamEvents]
type RedisStreamResults = list[RedisStreamResult]
