from nicegui import ui

_css = r"""
.scd-container {
    --ex-offset: 30px;
    --ex-rotate: 3deg;
    --ex-transition-duration: 0.3s;

    /* overflow-x: scroll; */
}

.scd-container .scd-target {

    /* box-shadow: -1rem 0 3rem -2rem #000; */
    transition: transform var(--ex-transition-duration) ease-in-out;
}


/* 从第二个卡片开始，每个往左偏移，做卡片重叠 */
.scd-container .scd-target:not(:first-child) {
    margin-left: calc(var(--ex-offset) * -1);
}

/*   鼠标悬停时，当前卡片之后的卡片往右偏移 */
.scd-container .scd-target:hover~.scd-target {
    transform: translateX(var(--ex-offset));
}

/*   鼠标悬停时，当前卡片旋转 */
.scd-container .scd-target:hover {
    transform: translate(-0.5rem, -1rem) rotate(var(--ex-rotate));
}
"""

ui.add_css(_css)


class SlidingCardDeck(ui.element):
    def __init__(self):
        super().__init__("div")
        self.classes("scd-container")

    @property
    def target_card_class(self):
        return "scd-target"


# Example usage:
if __name__ in {"__main__", "__mp_main__"}:
    with SlidingCardDeck() as hero_cards, ui.card().classes(
        "flex-row gap-2 p-8 scroll-x flex-wrap outline ring-2"
    ):
        for i in range(20):
            with ui.card().classes(
                "w-[10rem] h-[10rem] outline ring-offset-2 ring-2 ring-blue-500 shadow-2xl"
            ).classes(hero_cards.target_card_class):
                ui.label(f"Card {i+1}")

    ui.run()
