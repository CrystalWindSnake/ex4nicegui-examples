from nicegui import ui
from ex4nicegui import rxui, Ref


class foldable(rxui.grid):
    def __init__(self, show: Ref[bool], duration=0.3):
        """Create a foldable area with animateable height.

        Args:
            show (Ref[bool]):  A reference to a boolean value that controls whether the foldable area is shown or not.
            duration (float, optional): The duration of the animation when toggling the foldable area. Defaults to 0.3.
        """
        super().__init__()
        self.style(
            f"transition: grid-template-rows {duration}s ease-in-out;"
        ).bind_style({"grid-template-rows": lambda: "1fr" if show.value else "0fr"})

        self.__target_box = ui.element("div").style("overflow:hidden;")
        self.__target_box.move(self.element)

    def __enter__(self):
        return self.__target_box.__enter__()

    def __exit__(self, *args):
        return self.__target_box.__exit__(*args)


# Example usage:
if __name__ in {"__main__", "__mp_main__"}:
    from nicegui import ui
    from ex4nicegui import rxui, to_ref

    show = to_ref(True)

    rxui.switch(value=show)

    with foldable(show).classes("outline-red-500").bind_classes({"outline": show_xrw}):
        ui.label("This is the content of the foldable area.")
        ui.label("You can add more content here.")

    ui.run()
