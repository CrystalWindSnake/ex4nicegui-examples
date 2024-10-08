from systems.provider import provide
from ex4nicegui import to_ref, Ref
import vm
from typing import Literal

# app = provide(vm.TodoApp)
app = provide(lambda: vm.TodoApp.create_random_todos())

language: provide[Ref[Literal["en", "zh"]]] = provide(
    lambda: to_ref("zh"), scope="client"
)
