from pathlib import Path
from nicegui import ui, app
from ex4nicegui import rxui
import components
import utils
import provider

app.add_static_files(
    url_path="/static", local_directory=Path(__file__).parent / "static"
)


def setup_page():
    ui.add_css(".q-chip__content{ justify-content: center; }")

    utils.locked_page_height()
    ui.row.default_classes("items-center w-full")
    ui.input.default_props("outlined dense")
    ui.button.default_props("dense")

    ui.query("body").classes("overflow-y-hidden overflow-x-auto")
    ui.context.client.content.classes("items-center font-serif")
    ui.add_head_html('<link rel="stylesheet" href="/static/app.css">')

    for i in [20, 50, 80]:
        ui.label("ex4nicegui").classes("watermark-text").style(
            f"--top-offset:{i}%;--left-offset:{i}%"
        )


@ui.page("/")
def main_page():
    setup_page()
    todo_app = provider.app.get()

    with rxui.grid().classes(
        "h-full w-full min-w-[852px] max-w-[1200px] self-center target-card"
    ).bind_classes({"open": todo_app.statistics_card_opened}):
        # main view
        components.MainView()

        # statistics view
        components.StatisticsView()


ui.run()
