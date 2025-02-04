import asyncio
from collections.abc import Callable, Coroutine
from threading import Thread
from typing import Any

from click import Abort, Command, Group
from dishka import AsyncContainer
from dishka.integrations.base import is_dishka_injected, wrap_injection


def command_with_injected_dependencies_when(
    *,
    command: Command,
    container: AsyncContainer,
) -> Command:
    if command.callback is not None:
        command.callback = callback_with_injected_dependencies_when(
            callback=command.callback,
            container=container,
        )

    if isinstance(command, Group):
        for name, subcommand in command.commands.items():
            command.commands[name] = command_with_injected_dependencies_when(
                command=subcommand,
                container=container,
            )

    return command


def callback_with_injected_dependencies_when[R, **Pm](
    *,
    callback: Callable[Pm, Coroutine[Any, Any, R]],
    container: AsyncContainer,
) -> Callable[Pm, Any]:
    if is_dishka_injected(callback):
        return callback

    injected_callback = wrap_injection(
        func=callback,
        container_getter=lambda _, __: container,
        remove_depends=True,
        is_async=True,
    )

    return _marked_as_dishka_injected(in_isolated_event_loop(injected_callback))


def _marked_as_dishka_injected[V](value: V) -> V:
    value.__dishka_injected__ = True  # type: ignore[attr-defined]
    return value


def in_isolated_event_loop[R, **Pm](
    func: Callable[Pm, Coroutine[Any, Any, R]]
) -> Callable[Pm, None]:
    def wrapper(*args: Pm.args, **kwargs: Pm.kwargs) -> None:
        try:
            thread = Thread(target=lambda: asyncio.run(func(*args, **kwargs)))
            thread.start()
            thread.join()
        except Abort as abort:
            raise abort from None

    return wrapper
