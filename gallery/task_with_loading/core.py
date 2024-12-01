from typing import Any, Callable, Coroutine
from ex4nicegui.reactive.empty import Empty
from nicegui import ui, app
import asyncio


def _loading_view():
    ui.spinner("audio")


class LoadingTaskManager:
    def __init__(self, task_fn: Callable[..., Coroutine[Any, Any, None]]) -> None:
        self._task_fn = task_fn

    def view(self, fn: Callable):
        loadint_box = ui.element("div")
        with loadint_box:
            _loading_view()

        def _view():
            loadint_box.delete()
            with box:
                fn()

        box = Empty()

        if not ui.context.client.has_socket_connection:

            @app.on_connect
            async def connect():
                await self._task_fn()
                _view()
        else:
            task = asyncio.create_task(self._task_fn())

            def when_task_done(_):
                _view()

            task.add_done_callback(when_task_done)

        box = Empty()
