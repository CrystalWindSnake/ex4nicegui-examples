from typing import List, Literal, Optional
from ex4nicegui import Ref, rxui, deep_ref as ref, ReadonlyRef
import consts
import styles
import random
import itertools


class TodoItem(rxui.ViewModel):
    _ids = 0
    title = ""
    priority = ""
    completed = False
    title_editing = False

    def __init__(self, title: str, priority: str = consts.PRIORITYS[1]):
        super().__init__()

        self.title = title
        self.priority = priority

        self.id = self._ids
        TodoItem._ids += 1

    def show_title_edit(self):
        self.title_editing = True

    def hide_title_edit(self):
        self.title_editing = False

    def toggle_completed(self):
        self.completed = not self.completed

    def priority_color(self):
        return styles.get_priority_color(self.priority)


class TodoApp(rxui.ViewModel):
    todos: List[TodoItem] = []
    filter_type: Literal["all", "active", "completed"] = "all"
    title_input = ""
    statistics_card_opened = True

    _item_grid_col = "6ch auto 15ch 5ch"

    def __init__(self, todos: Optional[List[TodoItem]] = None):
        super().__init__()
        self.todos = todos or []

        self.is_title_input_valid = (
            lambda: self.title_input and len(self.title_input.strip()) > 0
        )

        self._pagination = rxui.use_pagination(self.filtered_todos, 7)
        self.records: ReadonlyRef[List[TodoItem]] = self._pagination.current_source

    def set_filter(self, filter_type: Literal["all", "active", "completed"]):
        self.filter_type = filter_type

    @staticmethod
    def create_random_todos():
        todos = [
            TodoItem(f"Task {i+1}", priority=random.choice(consts.PRIORITYS))
            for i in range(10)
        ]
        return TodoApp(todos)

    @rxui.cached_var
    def filtered_todos(self):
        sorted_todos = sorted(self.todos, key=lambda x: x.completed)
        return getattr(filters_service, self.filter_type)(sorted_todos)

    @rxui.cached_var
    def active_count(self):
        return len(filters_service.active(self.todos))

    @rxui.cached_var
    def completed_count(self):
        return len(filters_service.completed(self.todos))

    @rxui.cached_var
    def completion_ratio(self):
        if self.total_count() == 0:
            return 0
        return self.completed_count() / self.total_count()

    @rxui.cached_var
    def total_count(self):
        return len(filters_service.all(self.todos))

    @rxui.cached_var
    def is_all_checked(self):
        return all(item.completed for item in self.todos)

    def toggle_statistics_card(self):
        self.statistics_card_opened = not self.statistics_card_opened

    def priority_echarts_data(self):
        key_fn = lambda x: x.priority  # noqa: E731
        grouped = itertools.groupby(sorted(self.todos, key=key_fn), key_fn)

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
        self.todos.insert(0, TodoItem(title))

    def remove_item(self, item: TodoItem):
        self.todos.remove(item)

    def all_checks(self):
        for item in self.todos:
            item.completed = True

    def all_unchecks(self):
        for item in self.todos:
            item.toggle_completed()

    def add_task(self):
        title = self.title_input.strip()
        if title:
            self.add_item(title)
            self.title_input = ""

    def clear_completed(self):
        self.todos = [todo for todo in self.todos if not todo.completed]

    def delete_todo(self, item: TodoItem):
        self.todos.remove(item)


class filters_service:
    @staticmethod
    def active(todos: List[TodoItem]):
        return [todo for todo in todos if not todo.completed]

    @staticmethod
    def completed(todos: List[TodoItem]):
        return [todo for todo in todos if todo.completed]

    @staticmethod
    def all(todos: List[TodoItem]):
        return todos
