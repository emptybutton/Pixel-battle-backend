from dataclasses import dataclass

from pixel_battle.entities.space.time import Time


@dataclass(kw_only=True, frozen=True, slots=True)
class TimeDelta:
    start_time: Time
    end_time: Time

    def __contains__(self, time: Time) -> bool:
        return self.start_time <= time < self.end_time
