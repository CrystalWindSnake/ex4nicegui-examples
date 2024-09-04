from pathlib import Path
from ex4nicegui import (
    on,
    Ref,
    deep_ref as ref,
    rxui,
    to_value,
)
from signe.core.reactive import ListProxy, DictProxy
from nicegui import ui, app

import orjson
from decimal import Decimal
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")

app.add_static_file(
    local_file=Path(__file__).parent / "ex4localStorage.js",
    url_path="/ex4localStorage.js",
)
ui.add_body_html('<script src="/ex4localStorage.js"></script>', shared=True)


async def load_from_local_storage(key: str):
    return await ui.run_javascript(f"return ex4ng_loadDataFromLocalStorage(`{key}`)")


def _save_local_storage_with_dumps(key: str, data: str):
    ui.run_javascript(f"ex4ng_saveToLocalStorage(`{key}`, {data})")


def use_local_storage(
    key: str,
    initial_value: T,
    load_fn: Optional[Callable[[Any], T]] = None,
) -> Ref[T]:
    result = ref(initial_value)

    @ui.context.client.on_connect
    async def _():
        data = await load_from_local_storage(key)
        if load_fn and data:
            data = load_fn(data)

        if data:
            result.set_value(data)

    def save_fn():
        data = orjson.dumps(result.value, default=_orjson_converter).decode("utf-8")
        _save_local_storage_with_dumps(key, data)

    @on(save_fn, onchanges=True)
    def _():
        save_fn()

    return result


def _orjson_converter(obj):
    if isinstance(obj, Decimal):
        return float(obj)

    if isinstance(obj, ListProxy):
        return [item for item in obj]

    if isinstance(obj, DictProxy):
        return {key: value for key, value in obj.items()}

    if isinstance(obj, rxui.ViewModel):
        return {
            name: to_value(value)
            for name, value in vars(obj).items()
            if not name.startswith("_")
        }
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
