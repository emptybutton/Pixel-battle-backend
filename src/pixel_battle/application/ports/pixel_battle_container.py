from abc import ABC, abstractmethod

from pixel_battle.entities.core.pixel_battle import PixelBattle


class PixelBattleContainer(ABC):
    @abstractmethod
    async def put(self, pixel_battle: PixelBattle) -> None: ...

    @abstractmethod
    async def get(self) -> PixelBattle: ...
