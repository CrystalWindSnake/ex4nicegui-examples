from typing import List, Literal, Optional
from ex4nicegui import Ref, rxui, deep_ref as ref, ReadonlyRef
import consts
import styles
import random
import itertools


class TodoItem(rxui.ViewModel):
    _ids = 0

    def __init__(self, title: str, priority: str = consts.PRIORITYS[1]):
        super().__init__()

        self.title = ref(title)
        self.priority = ref(priority)
        self.completed = ref(False)
        self.title_editing = ref(False)

        self.id = self._ids
        TodoItem._ids += 1

    def show_title_edit(self):
        self.title_editing.value = True

    def hide_title_edit(self):
        self.title_editing.value = False

    def toggle_completed(self):
        self.completed.value = not self.completed.value

    def priority_color(self):
        return styles.get_priority_color(self.priority.value)


class TodoApp(rxui.ViewModel):
    def __init__(self, todos: Optional[List[TodoItem]] = None):
        super().__init__()
        self.todos = ref(todos or [])
        self.filter_type: Ref[Literal["all", "active", "completed"]] = ref("all")

        self.title_input = ref("")
        self.is_title_input_valid = (
            lambda: self.title_input.value is not None
            and len(self.title_input.value.strip()) > 0
        )
        self.statistics_card_opened = ref(True)
        self.item_grid_col = "6ch auto 15ch 5ch"

        self._pagination = rxui.use_pagination(self.filtered_todos, 7)
        self.records: ReadonlyRef[List[TodoItem]] = self._pagination.current_source

    @staticmethod
    def create_random_todos():
        todos = [
            TodoItem(f"Task {i+1}", priority=random.choice(consts.PRIORITYS))
            for i in range(10)
        ]
        return TodoApp(todos)

    @rxui.cached_var
    def filtered_todos(self):
        sorted_todos = sorted(self.todos.value, key=lambda x: x.completed.value)
        return getattr(filters_service, self.filter_type.value)(sorted_todos)

    @rxui.cached_var
    def active_count(self):
        return len(filters_service.active(self.todos.value))

    @rxui.cached_var
    def completed_count(self):
        return len(filters_service.completed(self.todos.value))

    @rxui.cached_var
    def completion_ratio(self):
        if self.total_count() == 0:
            return 0
        return self.completed_count() / self.total_count()

    @rxui.cached_var
    def total_count(self):
        return len(filters_service.all(self.todos.value))

    @rxui.cached_var
    def is_all_checked(self):
        return all(item.completed for item in self.todos.value)

    def toggle_statistics_card(self):
        self.statistics_card_opened.value = not self.statistics_card_opened.value

    def priority_echarts_data(self):
        key_fn = lambda x: x.priority.value  # noqa: E731
        grouped = itertools.groupby(sorted(self.todos.value, key=key_fn), key_fn)

        data = [
            {
                "value": sum(1 for _ in group),
                "name": key,
                "color": styles.get_priority_color(key).get_hex(),
            }
            for key, group in grouped
        ]

        return {
            "title": {
                "text": "priority distribution",
                "left": "center",
            },
            "tooltip": {"trigger": "item"},
            "legend": {"orient": "vertical", "left": "left"},
            "series": [
                {
                    "name": "priority",
                    "type": "pie",
                    "radius": "50%",
                    "data": data,
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)",
                        }
                    },
                    "itemStyle": {":color": "(item)=> item.data.color"},
                }
            ],
        }

    def todos_echarts_data(self):
        return {
            "legend": {"selectedMode": False},
            "grid": {"height": 30},
            "xAxis": {"type": "value", "show": False, "min": 0, "max": "dataMax"},
            "yAxis": {"type": "category", "data": ["Mon"], "show": False},
            "series": [
                {
                    "name": "completed",
                    "type": "bar",
                    "stack": "total",
                    "color": "#9bdb7d",
                    "data": [self.completed_count()],
                },
                {
                    "name": "active",
                    "type": "bar",
                    "stack": "total",
                    "color": "#5470c6",
                    "data": [self.active_count()],
                },
            ],
        }

    def add_item(self, title: str):
        self.todos.value.insert(0, TodoItem(title))

    def remove_item(self, item: TodoItem):
        self.todos.value.remove(item)

    def all_checks(self):
        for item in self.todos.value:
            item.completed.value = True

    def all_unchecks(self):
        for item in self.todos.value:
            item.toggle_completed()

    def add_task(self):
        title = self.title_input.value.strip()
        if title:
            self.add_item(title)
            self.title_input.value = ""

    def clear_completed(self):
        self.todos.value = [
            todo for todo in self.todos.value if not todo.completed.value
        ]

    def delete_todo(self, item: TodoItem):
        self.todos.value.remove(item)


class filters_service:
    @staticmethod
    def active(todos: List[TodoItem]):
        return [todo for todo in todos if not todo.completed.value]

    @staticmethod
    def completed(todos: List[TodoItem]):
        return [todo for todo in todos if todo.completed.value]

    @staticmethod
    def all(todos: List[TodoItem]):
        return todos
