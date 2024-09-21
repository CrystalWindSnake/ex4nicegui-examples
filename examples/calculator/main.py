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


def use_view_model_object():
    class Vm(rxui.ViewModel):
        num1 = 0
        num2 = 0
        sign = "+"
        error = ""

        @rxui.cached_var
        def result(self):
            self.error = ""
            try:
                return calculate(self.num1, self.num2, self.sign)
            except Exception as e:
                self.error = (
                    f'Error by evaluating "{self.num1}{self.sign}{self.num2}": {e}'
                )
                return "N/A"

        def has_error(self):
            return bool(self.error)

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

        with ui.expansion("use_view_model_object", group="calculate"):
            use_view_model_object()

    ui.run()
