from ex4nicegui import rxui, to_ref, deep_ref as ref
from nicegui import ui
import utils.example_panles as ex_panels

panels = ex_panels.Panels()


ui.number.default_props("outlined")
ui.select.default_props("outlined")


@panels.example
def base():
    num1 = to_ref(0)
    num2 = to_ref(0)
    sign = to_ref("+")

    def add():
        try:
            return eval(f"{num1.value}{sign.value}{num2.value}")
        except Exception as e:
            return f'Error by evaluating "{num1.value}{sign.value}{num2.value}": {e}'

    def has_error():
        return isinstance(add(), str)

    # ==== UI ====
    ui.number.default_props("outline")

    with ui.row(align_items="center"):
        rxui.number(value=num1)
        rxui.select(["+", "-", "*", "/"], value=sign)
        rxui.number(value=num2)
        ui.label("=")
        rxui.label(add).bind_color(lambda: "red" if has_error() else "black")


@panels.example
def use_view_model_class():
    class Data(rxui.ViewModel):
        num1 = ref(0)
        num2 = ref(0)
        sign = to_ref("+")

        @classmethod
        def add(cls):
            try:
                return eval(f"{cls.num1.value}{cls.sign.value}{cls.num2.value}")
            except Exception as e:
                return f'Error by evaluating "{cls.num1.value}{cls.sign.value}{cls.num2.value}": {e}'

        @classmethod
        def has_error(cls):
            return isinstance(cls.add(), str)

    # ==== UI ====
    ui.number.default_props("outline")

    with ui.row(align_items="center"):
        rxui.number(value=Data.num1)
        rxui.select(["+", "-", "*", "/"], value=Data.sign)
        rxui.number(value=Data.num2)
        ui.label("=")
        rxui.label(Data.add).bind_color(lambda: "red" if Data.has_error() else "black")


@panels.example
def use_view_model_object():
    class Data(rxui.ViewModel):
        num1 = ref(0)
        num2 = ref(0)
        sign = to_ref("+")

        def add(self):
            try:
                return eval(f"{self.num1.value}{self.sign.value}{self.num2.value}")
            except Exception as e:
                return f'Error by evaluating "{self.num1.value}{self.sign.value}{self.num2.value}": {e}'

        def has_error(self):
            return isinstance(self.add(), str)

    data = Data()

    # ==== UI ====
    ui.number.default_props("outline")

    with ui.row(align_items="center"):
        rxui.number(value=data.num1)
        rxui.select(["+", "-", "*", "/"], value=data.sign)
        rxui.number(value=data.num2)
        ui.label("=")
        rxui.label(data.add).bind_color(lambda: "red" if data.has_error() else "black")
