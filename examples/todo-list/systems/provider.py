from typing import Any, Callable, TypeVar, Literal, Generic
import functools
import weakref
from nicegui import Client as ng_Client, ui

T = TypeVar("T")
T_Provider_Scope = Literal["global", "client"]


class ProvideDescriptor(Generic[T]):
    def __init__(self, builder: Callable[..., T], scope: T_Provider_Scope = "client"):
        if scope == "global":
            builder = functools.lru_cache(maxsize=1)(builder)
        elif scope == "client":
            client_map: weakref.WeakKeyDictionary[
                ng_Client, Any
            ] = weakref.WeakKeyDictionary()

            original_builder = builder

            def new_builder():
                current_client = ui.context.client
                if current_client not in client_map:
                    client_map[current_client] = original_builder()
                return client_map[current_client]

            builder = new_builder

        else:
            raise ValueError(f"Invalid scope: {scope}")

        self.builder = builder
        self.scope = scope

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.builder()

    def __set__(self, instance, value):
        raise AttributeError("Can't set attribute")

    def get(self) -> T:
        return self.builder()


provide = ProvideDescriptor

# def provide(
#     builder: Callable[..., T], scope: T_Provider_Scope = "client"
# ) -> ProvideDescriptor[T]:
#     return ProvideDescriptor(builder, scope)


def provide_descriptor(
    builder: Callable[..., T], scope: T_Provider_Scope = "client"
) -> T:
    return ProvideDescriptor(builder, scope)  # type: ignore
