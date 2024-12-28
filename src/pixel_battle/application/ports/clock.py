from abc import ABC, abstractmethod

from pixel_battle.entities.quantities.time import Time


class Clock(ABC):
    @abstractmethod
    async def get_current_time(self) -> Time: ...
