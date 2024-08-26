from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from nicegui import ui
from ex4nicegui import (
    on,
    rxui,
    TMaybeRef,
    effect_refreshable,
    ref_computed as computed,
)
import consts
import provider
from translates import Translates

if TYPE_CHECKING:
    import vm


def todo_item(todo_app: vm.TodoApp, todo: vm.TodoItem):
    with rxui.card().classes("x-todo-item w-full").bind_classes(
        lambda: f"bg-gradient-to-r from-[{todo.priority_color().get_hex()}] from-10%"
    ).bind_style(
        {"background-color": lambda: todo.priority_color().get_rgba(alpha=0.5)}
    ), ui.grid(columns=todo_app.item_grid_col).classes("w-full"):
        # checkbox and title
        rxui.checkbox(value=todo.completed)
        with ui.row(align_items="center").classes("gap-1 relative overflow-hidden"):
            with rxui.row(wrap=False).classes("gap-1").bind_not_visible(
                todo.title_editing
            ).on("click", todo.show_title_edit):
                rxui.label(todo.title).classes(
                    "grow cursor-pointer select-none truncate"
                ).bind_classes({"line-through": todo.completed})
                rxui.button(icon="edit").classes("x-edit-btn").props("flat round dense")

            # editor
            TodoEdit(todo)

        # priority
        rxui.select(consts.PRIORITYS, value=todo.priority).props("dense outlined")

        # delete action
        with rxui.button(
            icon="delete",
            color=lambda: "negative" if todo.completed.value else "grey-4",
            on_click=lambda: todo_app.delete_todo(todo),
        ).props("flat round dense").bind_enabled(todo.completed):
            rxui.tooltip(Translates.todo_item_del_tooltip).bind_not_visible(
                todo.completed
            )


class MainView:
    def __init__(self):
        todo_app = provider.app.get()

        with rxui.card().classes(
            "items-center h-full backdrop-blur-sm bg-white/30 gap-1 w-full relative overflow-hidden"
        ):
            with ui.row(align_items="center").classes("justify-between  py-2"):
                rxui.select(
                    {"en": "english", "zh": "中文"}, value=provider.language.get()
                ).props("dense outlined")
                rxui.label(Translates.app_title).classes("text-3xl font-bold")
                StatisitcsOpenButton()

            # input
            NewTaskInput()

            # filters
            TaskFilterChoice()

            # statistics
            with ui.row(align_items="center").classes("h-[3rem]"):
                rxui.label(
                    lambda: f"{len(todo_app.filtered_todos())} {todo_app.filter_type.value} {Translates.filter_label()}"
                )
                ui.space()
                rxui.button(
                    Translates.clear_completed_button_text,
                    on_click=todo_app.clear_completed,
                ).props("outline rounded dense").classes("px-4").bind_visible(
                    lambda: todo_app.completed_count() > 0
                )

            # todos list table
            TodoItemsTable()

            todo_app._pagination.create_q_pagination().bind_visible(
                lambda: todo_app._pagination.page_count.value > 1
            )


class StatisticsView:
    def __init__(self):
        todo_app = provider.app.get()

        with ui.element("div"), ui.card().classes(
            "h-full backdrop-blur-sm bg-white/30 gap-1 "
        ):
            rxui.label(Translates.statistics_card_title).classes("text-3xl font-bold")

            PriorityStatisticsChart()

            with ui.row(wrap=False).classes("font-[Roboto] w-full justify-around"):
                StatisticsText(
                    todo_app.completed_count,
                    Translates.statistics_card_completed_text,
                    "check_circle",
                    "#65a30d",
                ).box.on(
                    "click", lambda: todo_app.filter_type.set_value("completed")
                ).tooltip(Translates.statistics_card_text_tooltip)

                StatisticsText(
                    todo_app.active_count,
                    Translates.statistics_card_active_text,
                    "hourglass_empty",
                ).box.on(
                    "click", lambda: todo_app.filter_type.set_value("active")
                ).tooltip(Translates.statistics_card_text_tooltip)

                StatisticsText(
                    todo_app.total_count,
                    Translates.statistics_card_total_text,
                    "view_list",
                ).box.on(
                    "click", lambda: todo_app.filter_type.set_value("all")
                ).tooltip(Translates.statistics_card_text_tooltip)

            TodosStatisticsChart()


class StatisitcsOpenButton:
    def __init__(self):
        todo_app = provider.app.get()
        # statistics button
        rxui.button(
            icon="menu_open",
            on_click=todo_app.toggle_statistics_card,
        ).classes(
            "transition-transform duration-300 ease-in-out place-self-center"
        ).props('rounded size="lg"').bind_classes(
            {"rotate-180": lambda: not todo_app.statistics_card_opened.value}
        )


class TodoEdit:
    def __init__(self, todo: vm.TodoItem) -> None:
        super().__init__()
        self.todo = todo
        self.input_title_edit = None

        @on(todo.title_editing, onchanges=True)
        def _():
            if todo.title_editing.value:
                self.input_title_edit.element.run_method("focus")  # type: ignore

        self.view()

    def view(self):
        with rxui.row(wrap=False).classes("absolute inset-0 z-10").bind_visible(
            self.todo.title_editing
        ):
            self.input_title_edit = (
                rxui.lazy_input(value=self.todo.title)
                .classes("grow")
                .on("blur", self.todo.hide_title_edit)
                .on("keyup.enter", self.todo.hide_title_edit)
            )
            rxui.button(icon="check", on_click=self.todo.hide_title_edit)


class NewTaskInput:
    def __init__(self):
        todo_app = provider.app.get()
        with ui.row(wrap=False).classes("max-w-[80ch]"):
            rxui.input(
                value=todo_app.title_input,
                placeholder=Translates.add_task_input_placeholder,
            ).classes("grow").on("keyup.enter", todo_app.add_task)

            rxui.button(icon="add", on_click=todo_app.add_task).bind_enabled(
                lambda: bool(todo_app.title_input.value.strip())
            )


class TaskFilterChoice:
    def __init__(self):
        todo_app = provider.app.get()

        with ui.row(align_items="center").classes("justify-center"):
            rxui.radio(self.options(), value=todo_app.filter_type).props("inline")

    def options(self):
        @computed
        def options():
            return {
                "all": Translates.filter_type_all(),
                "active": Translates.filter_type_active(),
                "completed": Translates.filter_type_completed(),
            }

        return options


class TodoItemsTable:
    def __init__(self):
        todo_app = provider.app.get()

        # header
        with rxui.card().classes("w-full py-1 bg-gray-800"), ui.grid(
            columns=todo_app.item_grid_col
        ).classes("w-full"):
            self._header_title(Translates.items_table_header_check)
            self._header_title(Translates.items_table_header_title)
            self._header_title(Translates.items_table_header_priority)
            rxui.label("")

        # list items
        with rxui.column(wrap=False).classes(
            "w-full grow items-stretch bg-transparent"
        ).bind_visible(
            lambda: len(todo_app.filtered_todos()) > 0
        ), ui.scroll_area().classes("h-full"):

            @effect_refreshable.on(todo_app.records)
            def _():
                for todo in todo_app.records.value:
                    todo_item(todo_app, todo)

            # @rxui.vfor(todo_app.records, key="id")
            # def each_todo(s: rxui.VforStore[vm.TodoItem]):
            #     todo = s.get_item()
            #     components.todo_item(todo_app, todo)

    def _header_title(self, text: TMaybeRef[str]):
        rxui.label(text).classes("text-left text-white font-bold ")


class StatisticsText:
    def __init__(
        self,
        number: TMaybeRef[float],
        text: TMaybeRef[str],
        icon: str,
        main_color: Optional[str] = None,
    ):
        super().__init__()

        with rxui.column().classes(
            "bg-transparent gap-0 cursor-pointer items-center"
        ) as self.box:
            ui.icon(icon, size="4rem", color=main_color or "gray-500")
            lbl_number = (
                rxui.label(number).classes("font-bold").style("font-size: 2.5rem;")
            )
            rxui.label(text).classes("text-gray-500 text-sm")

        if main_color:
            lbl_number.classes(f"text-[{main_color}]")


class PriorityStatisticsChart:
    def __init__(self):
        todo_app = provider.app.get()

        with ui.card().classes("w-full bg-transparent"):
            rxui.echarts(todo_app.priority_echarts_data)


class TodosStatisticsChart:
    def __init__(self):
        todo_app = provider.app.get()

        with ui.card().classes("w-full bg-transparent h-[150px]"):
            rxui.echarts(todo_app.todos_echarts_data)
