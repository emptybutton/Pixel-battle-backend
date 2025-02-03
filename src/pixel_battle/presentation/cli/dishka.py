import asyncio
from collections.abc import Callable, Coroutine
from copy import deepcopy
from threading import Thread
from typing import Any

from click import Command
from dishka import AsyncContainer
from dishka.integrations.base import wrap_injection


def command_with_injected_dependencies_when(
    *,
    container: AsyncContainer,
    command: Command,
) -> Command:
    if command.callback is None:
        return command

    command_to_mutate = deepcopy(command)
    command_to_mutate.callback = callback_with_injected_dependencies_when(
        callback=command.callback,
        container=container,
    )

    return command_to_mutate


def callback_with_injected_dependencies_when[R, **Pm](
    *,
    callback: Callable[Pm, Coroutine[Any, Any, R]],
    container: AsyncContainer,
) -> Callable[Pm, None]:
    injected_callback = wrap_injection(
        func=callback,
        container_getter=lambda _, __: container,
        remove_depends=True,
        is_async=True,
    )

    return in_isolated_event_loop(injected_callback)


def in_isolated_event_loop[R, **Pm](
    func: Callable[Pm, Coroutine[Any, Any, R]]
) -> Callable[Pm, R]:
    def wrapper(*args: Pm.args, **kwargs: Pm.kwargs) -> None:
        thread = Thread(target=lambda: asyncio.run(func(*args, **kwargs)))
        thread.start()
        thread.join()

    return wrapper
