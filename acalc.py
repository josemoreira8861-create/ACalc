import tkinter as tk
from tkinter import ttk

from inputframes import (
    FrameEsferas,
    FrameRoda,
    FrameEngrenagem,
    FrameSemFim,
    FrameRollete,
    FrameReishauer,
)

from cotas import COTAS
from rodasdemuda import RODAS

from resultframes import RESULT_FRAMES


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ACalc")
        self.geometry("1200x700")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=3)
        self.rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = Sidebar(self, self.load_frame)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Input area
        self.content = ttk.Frame(self)
        self.content.grid(row=0, column=1, sticky="nsew")

        # Results area
        self.results_frame = None
        self.current_tool = None

        self.current_frame = None

    # ---------------- LOAD INPUT FRAME ----------------
    def load_frame(self, frame_class):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = frame_class(self.content, self.handle_calculate)
        self.current_frame.grid(sticky="nsew")

    # ---------------- ROUTER ----------------
    def handle_calculate(self, tool, data):

        # Decide which calculator set to use
        calc_class = (
            COTAS.get(tool)
            or RODAS.get(tool)
        )

        if not calc_class:
            return

        result = calc_class(data).calculate()

        # Switch results frame if needed
        if tool != self.current_tool:
            if self.results_frame:
                self.results_frame.destroy()

            frame_class = RESULT_FRAMES.get(tool)

            if frame_class:
                self.results_frame = frame_class(self)
                self.results_frame.grid(row=0, column=2, sticky="nsew")

            self.current_tool = tool

        if self.results_frame:
            self.results_frame.show_results(result)


# ---------------- SIDEBAR ----------------
class Sidebar(ttk.Frame):
    def __init__(self, parent, load_callback):
        super().__init__(parent)

        self.load_callback = load_callback

        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="Ferramentas").grid(row=0, column=0)

        # Combobox 1
        ttk.Label(self, text="Cotas de verificação").grid(row=1, column=0)

        self.cb1 = ttk.Combobox(self, state="readonly")
        self.cb1["values"] = ["Esferas", "Ek Roda Dentada", "Ek Engrenagem", "Ek Sem-fim"]
        self.cb1.grid(row=1, column=1)

        # Combobox 2
        ttk.Label(self, text="Cotas de muda").grid(row=2, column=0)

        self.cb2 = ttk.Combobox(self, state="readonly")
        self.cb2["values"] = ["Rollete", "Reishauer"]
        self.cb2.grid(row=2, column=1)

        self.frames_map = {
            "Esferas": FrameEsferas,
            "Ek Roda Dentada": FrameRoda,
            "Ek Engrenagem": FrameEngrenagem,
            "Ek Sem-fim": FrameSemFim,
            "Rollete": FrameRollete,
            "Reishauer": FrameReishauer,
        }

        self.cb1.bind("<<ComboboxSelected>>", self.on_select)
        self.cb2.bind("<<ComboboxSelected>>", self.on_select)

    def on_select(self, event):
        if event.widget == self.cb1:
            self.cb2.set("")
            value = self.cb1.get()
        else:
            self.cb1.set("")
            value = self.cb2.get()

        frame_class = self.frames_map.get(value)

        if frame_class:
            self.load_callback(frame_class)


if __name__ == "__main__":
    Application().mainloop()