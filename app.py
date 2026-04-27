import tkinter as tk
from tkinter import ttk

from frames import (
    FrameEsferas,
    FrameRoda,
    FrameEngrenagem,
    FrameSemFim,
    FrameRollete,
    FrameReishauer,
)

from cotas import COTAS


def main():
    app = Application()
    app.mainloop()


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ACalc")
        self.geometry("1200x700")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = Sidebar(self, self.load_frame)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Content area
        self.content = ttk.Frame(self)
        self.content.grid(row=0, column=1, sticky="nsew")

        self.current_frame = None

    # ---------------- FRAME LOADER ----------------
    def load_frame(self, frame_class):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = frame_class(self.content, self.handle_calculate)
        self.current_frame.pack(fill="both", expand=True)

    # ---------------- CALCULATION ROUTER ----------------
    def handle_calculate(self, tool, data):
        calc_class = COTAS.get(tool)

        if calc_class:
            result = calc_class(data).calculate()
            print(f"{tool} result:", result)


# ---------------- SIDEBAR ----------------
class Sidebar(ttk.Frame):
    def __init__(self, parent, load_callback):
        super().__init__(parent)

        self.load_callback = load_callback
        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="Ferramentas").grid(row=0, column=0, sticky="ew")

        # Combobox 1
        ttk.Label(self, text="Cotas de verificação").grid(row=1, column=0, sticky="ew")

        self.cb1 = ttk.Combobox(self, state="readonly")
        self.cb1["values"] = [
            "Esferas",
            "Ek Roda Dentada",
            "Ek Engrenagem",
            "Ek Sem-fim",
        ]
        self.cb1.grid(row=1, column=1, sticky="ew")

        # Combobox 2
        ttk.Label(self, text="Cotas de muda").grid(row=2, column=0, sticky="ew")

        self.cb2 = ttk.Combobox(self, state="readonly")
        self.cb2["values"] = [
            "Rollete",
            "Reishauer",
        ]
        self.cb2.grid(row=2, column=1, sticky="ew")

        # Map combobox values → frames
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
        # Clear opposite combobox (mutual exclusivity)
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
    main()