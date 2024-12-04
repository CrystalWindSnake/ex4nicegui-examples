from typing import Any, Callable, Awaitable, Union
from ex4nicegui import rxui, to_ref, to_value, async_computed, Ref
from nicegui import run
from nicegui.helpers import is_coroutine_function
from nicegui.functions.refreshable import RefreshableContainer


class LoadingView(RefreshableContainer):
    def __init__(self, evaluating: Ref[bool]):
        super().__init__()
        self.box = rxui.element("div").bind_visible(evaluating)

    def __enter__(self):
        self.box.element.clear()

        return self.box.__enter__()


class ProgressIndicator:
    def __init__(
        self, long_time_task: Callable[..., Union[Any, Awaitable]], *args: Ref
    ):
        self.__evaluating = to_ref(False)

        @async_computed(args, evaluating=self.__evaluating)
        async def result():
            if is_coroutine_function(long_time_task):
                return await long_time_task(*[to_value(arg) for arg in args])  # type: ignore

            return await run.io_bound(long_time_task, *[to_value(arg) for arg in args])

        self.__result = result

    @property
    def evaluating(self):
        """A boolean value that indicates if the long running task is running."""
        return self.__evaluating

    @property
    def result(self):
        """The result of the long running task."""
        return self.__result

    def loading_view(self):
        """A loading view that shows while the long running task is running."""
        container = LoadingView(self.__evaluating)
        with container:
            rxui.element("q-spinner-bars")

        return container


# Example usage:
if __name__ in {"__main__", "__mp_main__"}:
    from nicegui import ui
    import asyncio
    from time import sleep

    # data processing
    def long_running_task(text: str):
        sleep(3)
        return text + "done"

    async def async_long_running_task(text: str):
        await asyncio.sleep(3)
        return text + "done async"

    # ui state
    text = to_ref("hello")
    progress_indicator = ProgressIndicator(async_long_running_task, text)

    # ui
    rxui.input(value=text)

    progress_indicator.loading_view()
    # with io_bound_task.loading_view():
    #     rxui.label("正在查询...")

    rxui.label(progress_indicator.result).bind_visible(
        lambda: bool(progress_indicator.result.value)
        and (not progress_indicator.evaluating.value)
    )

    ui.button("查询")

    ui.run()
