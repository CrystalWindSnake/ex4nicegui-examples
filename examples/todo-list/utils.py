from typing import Optional
from nicegui import ui
from colorsys import hls_to_rgb
import fastapi


def locked_page_height():
    """
    Sets the height of the page to 100vh
    """
    client = ui.context.client
    q_page = client.page_container.default_slot.children[0]
    q_page.props(
        ''':style-fn="(offset, height) => ( { height: offset ? `calc(100vh - ${offset}px)` : '100vh' })"'''
    )
    client.content.classes("h-full")


def is_zh_client_language(request: fastapi.Request):
    accept_language = request.headers.get("accept-language")
    if not accept_language:
        return False
    languages = accept_language.split(",")

    return any("zh" in lang for lang in languages)


def hsl2rgba(
    h_degrees: float, saturation: float, lightness: float, alpha: Optional[float] = None
):
    h = h_degrees / 360.0

    r, g, b = hls_to_rgb(h, lightness, saturation)
    if alpha is None:
        return f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"
    return f"rgba({int(r*255)}, {int(g*255)}, {int(b*255)}, {alpha})"


def hsl2hex(h_degrees: float, saturation: float, lightness: float):
    h = h_degrees / 360.0

    r, g, b = hls_to_rgb(h, lightness, saturation)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
