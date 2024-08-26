class ElementView:
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        original_init = getattr(cls, "__init__", None)

        if original_init:

            def new_init(self, *args, **kwargs):
                original_init(self, *args, **kwargs)
                self.__view()

            cls.__init__ = new_init

    def view(self):
        raise NotImplementedError()

    def __view(self):
        self.view()
        self._view_runned = True
