from typing import Optional
import utils

_PRIORITY_COLORS = {
    "high": (0, 0.7222, 0.70),
    "medium": (270, 0.9524, 0.7529),
    "low": (82.71, 0.7797, 0.5549),
}


class Color:
    def __init__(
        self,
        h_degrees: float,
        saturation: float,
        lightness: float,
    ):
        self.h_degrees = h_degrees
        self.saturation = saturation
        self.lightness = lightness

    def get_rgba(self, alpha: Optional[float] = None) -> str:
        return utils.hsl2rgba(self.h_degrees, self.saturation, self.lightness, alpha)

    def get_hex(self):
        return utils.hsl2hex(self.h_degrees, self.saturation, self.lightness)


def get_priority_color(priority: str) -> Color:
    color_tuple = _PRIORITY_COLORS.get(priority, None)
    assert color_tuple, f"Invalid priority: {priority}"
    return Color(*color_tuple)
