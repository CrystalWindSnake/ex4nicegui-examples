from pathlib import Path
from nicegui import ui, app
import components
import utils
import provider
import fastapi


@app.on_startup
def _():
    app.add_static_files(
        url_path="/static", local_directory=Path(__file__).parent / "static"
    )

    ui.add_head_html('<link rel="stylesheet" href="/static/app.css">', shared=True)
    ui.row.default_classes("items-center w-full")
    ui.input.default_props("outlined dense")
    ui.button.default_props("dense")


def setup_page():
    utils.locked_page_height()

    ui.query("body").classes("overflow-y-hidden overflow-x-auto")
    ui.context.client.content.classes("items-center font-serif")

    # add watermark
    for i in [20, 50, 80]:
        ui.label("ex4nicegui").classes("watermark-text").style(
            f"--top-offset:{i}%;--left-offset:{i}%"
        )


@ui.page("/")
def main_page(request: fastapi.Request):
    setup_page()

    provider.language.get().set_value(
        "zh" if utils.is_zh_client_language(request) else "en"
    )

    components.AppView()


ui.run()
