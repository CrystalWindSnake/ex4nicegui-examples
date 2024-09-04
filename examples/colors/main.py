from nicegui import ui
from ex4nicegui import rxui, to_ref

ui.query("body").classes("bg-gray-100")

ui.radio.default_props("inline")

colors = ["red", "green", "blue", "yellow", "purple", "white"]

color = to_ref("blue")
bg_color = to_ref("red")


# Within the function, accessing `ref` or other associated functions will automatically synchronize updates
def bg_text():
    return f"Current background color is {bg_color.value}"


# UI

with ui.row(align_items="center"):
    rxui.radio(colors, value=color)
    ## With lambda
    rxui.label(lambda: f"Font color is {color.value}").bind_style({"color": color})

with ui.row(align_items="center"):
    rxui.radio(colors, value=bg_color)
    ## With function
    rxui.label(bg_text).bind_style({"background-color": bg_color})


ui.run()
