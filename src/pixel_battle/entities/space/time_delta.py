from dataclasses import dataclass

from pixel_battle.entities.space.time import Time


class StartAfterEndTimeDeltaError(Exception): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class TimeDelta:
    start_time: Time
    end_time: Time

    def __post_init__(self) -> None:
        if self.start_time > self.end_time:
            raise StartAfterEndTimeDeltaError

    def __contains__(self, time: Time) -> bool:
        return self.start_time <= time < self.end_time
