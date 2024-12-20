from pytest import fixture

from pixel_battle.application.interactors.recolor_pixel import RecolorPixel
from pixel_battle.infrastructure.adapters.broker import InMemoryBroker


@fixture
def recolor_pixel() -> RecolorPixel:
    return RecolorPixel(broker=InMemoryBroker())
