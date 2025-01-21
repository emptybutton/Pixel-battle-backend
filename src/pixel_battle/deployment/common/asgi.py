from collections.abc import Awaitable, MutableMapping
from dataclasses import dataclass, field
from typing import Any, Callable


Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]

Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]


@dataclass(kw_only=True)
class LazyASGIApp:
    factory: Callable[[], Awaitable[ASGIApp]]
    __app: ASGIApp | None = field(default=None, init=False)

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        if self.__app is None:
            self.__app = await self.factory()

        await self.__app(scope, receive, send)
