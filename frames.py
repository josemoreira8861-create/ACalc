from tkinter import ttk


class FrameEsferas(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Frame Esferas").pack()


class FrameRoda(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Frame Roda Dentada").pack()


class FrameEngrenagem(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Frame Engrenagem").pack()


class FrameSemFim(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Frame Sem-fim").pack()


class FrameRollete(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Frame Rollete").pack()


class FrameReishauer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Frame Reishauer").pack()