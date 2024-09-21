from nicegui import ui
from ex4nicegui import rxui


# 数据状态代码
class Counter(rxui.ViewModel):
    count: int = 0

    @rxui.cached_var
    def text_color(self):
        if self.count > 0:
            return "green"
        elif self.count < 0:
            return "red"
        else:
            return "black"

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1


# 界面代码
ui.button.default_props("round outline size=xs")
counter = Counter()

with ui.row(align_items="center"):
    ui.button(icon="remove", on_click=counter.decrement)
    rxui.label(counter.count).bind_color(counter.text_color)
    ui.button(icon="add", on_click=counter.increment)

rxui.label(lambda: f"count: {counter.count}").bind_color(counter.text_color)


ui.run()
