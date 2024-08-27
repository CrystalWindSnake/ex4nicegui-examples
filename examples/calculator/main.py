from ex4nicegui import rxui, to_ref
from nicegui import ui

ui.number.default_props("outlined")
ui.select.default_props("outlined")


def calculate(a: int, b: int, sign: str):
    return eval(f"{a}{sign}{b}")


def base():
    num1 = to_ref(0)
    num2 = to_ref(0)
    sign = to_ref("+")
    error = to_ref("")
    has_error = lambda: bool(error.value)

    def result():
        error.value = ""
        try:
            return calculate(num1.value, num2.value, sign.value)
        except Exception as e:
            error.value = (
                f'Error by evaluating "{num1.value}{sign.value}{num2.value}": {e}'
            )
            return "N/A"

    # ==== UI ====

    with ui.row(align_items="center"):
        rxui.number(value=num1)
        rxui.select(["+", "-", "*", "/"], value=sign)
        rxui.number(value=num2)
        ui.label("=")
        rxui.label(result)

    rxui.label(error).bind_color(
        lambda: "red" if has_error() else "black"
    ).bind_visible(has_error)


def use_view_model_class():
    class Vm(rxui.ViewModel):
        num1 = rxui.var(0)
        num2 = rxui.var(0)
        sign = rxui.var("+")
        error = rxui.var("")

        @classmethod
        def result(cls):
            cls.error.value = ""
            try:
                return calculate(cls.num1.value, cls.num2.value, cls.sign.value)
            except Exception as e:
                cls.error.value = f'Error by evaluating "{cls.num1.value}{cls.sign.value}{cls.num2.value}": {e}'
                return "N/A"

        @classmethod
        def has_error(cls):
            return bool(cls.error.value)

    # ==== UI ====
    ui.number.default_props("outline")

    with ui.row(align_items="center"):
        rxui.number(value=Vm.num1)
        rxui.select(["+", "-", "*", "/"], value=Vm.sign)
        rxui.number(value=Vm.num2)
        ui.label("=")
        rxui.label(Vm.result).bind_color(lambda: "red" if Vm.has_error() else "black")

    rxui.label(Vm.error).bind_color(
        lambda: "red" if Vm.has_error() else "black"
    ).bind_visible(Vm.has_error)


def use_view_model_object():
    class Vm(rxui.ViewModel):
        num1 = rxui.var(0)
        num2 = rxui.var(0)
        sign = rxui.var("+")
        error = rxui.var("")

        @rxui.cached_var
        def result(self):
            self.error.value = ""
            try:
                return calculate(self.num1.value, self.num2.value, self.sign.value)
            except Exception as e:
                self.error.value = f'Error by evaluating "{self.num1.value}{self.sign.value}{self.num2.value}": {e}'
                return "N/A"

        def has_error(self):
            return bool(self.error.value)

    vm = Vm()

    # ==== UI ====
    ui.number.default_props("outline")

    with ui.row(align_items="center"):
        rxui.number(value=vm.num1)
        rxui.select(["+", "-", "*", "/"], value=vm.sign)
        rxui.number(value=vm.num2)
        ui.label("=")
        rxui.label(vm.result).bind_color(lambda: "red" if vm.has_error() else "black")

    rxui.label(vm.error).bind_color(
        lambda: "red" if vm.has_error() else "black"
    ).bind_visible(vm.has_error)


if __name__ in {"__main__", "__mp_main__"}:
    with ui.card().classes("w-full items-stretch"):
        with ui.expansion("base", group="calculate"):
            base()

        with ui.expansion("use_view_model_class", group="calculate"):
            use_view_model_class()

        with ui.expansion("use_view_model_object", group="calculate"):
            use_view_model_object()

    ui.run()
