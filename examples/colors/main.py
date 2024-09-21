from nicegui import ui
from ex4nicegui import rxui, to_ref


class ColorElement(rxui.ViewModel):
    _colors = ["red", "green", "blue", "yellow", "purple", "white"]
    color = to_ref("blue")
    bg_color = to_ref("red")

    def __init__(self):
        super().__init__()
        self._create()

    def bg_text(self):
        return f"Current background color is {self.bg_color}"

    def _create(self):
        with ui.row(align_items="center"):
            rxui.radio(self._colors, value=self.color)
            ## With lambda
            rxui.label(lambda: f"Font color is {self.color}").bind_style(
                {"color": self.color}
            )

        with ui.row(align_items="center"):
            rxui.radio(self._colors, value=self.bg_color)
            ## With function
            rxui.label(self.bg_text).bind_style({"background-color": self.bg_color})


# UI
ui.query("body").classes("bg-gray-100")
ui.radio.default_props("inline")


ColorElement()

ui.run()
