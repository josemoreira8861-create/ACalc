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

        # Frame para selecionar a ferramenta
        self.sidebar = Sidebar(self, self.load_frame)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Frame dos parametros a inserir
        self.content = ttk.Frame(self)
        self.content.grid(row=0, column=1, sticky="nsew")

        self.current_frame = None

    def load_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = frame_class(self.content)
        self.current_frame.pack(fill="both", expand=True)

# Frame para selecionar as ferramentas
class Sidebar(ttk.Frame):
    def __init__(self, parent, load_callback):
        super().__init__(parent)

        self.load_callback = load_callback

        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="Ferramentas").grid(row=0, column=0, sticky="ew")

        ttk.Label(self, text="Cotas de verificação:").grid(row=1, column=0, sticky="ew")

        self.dimensoes_controlo_cb = ttk.Combobox(self, state="readonly")
        self.dimensoes_controlo_cb["values"] = (
            "Esferas",
            "Ek Roda Dentada",
            "Ek Engrenagem",
            "Ek Sem-fim",
        )
        self.dimensoes_controlo_cb.grid(row=1, column=1, sticky="ew")

        ttk.Label(self, text="Cotas de muda").grid(row=2, column=0, sticky="ew")

        self.cotasdemuda_cb = ttk.Combobox(self, state="readonly")
        self.cotasdemuda_cb["values"] = (
            "Rollete",
            "Reishauer",
            "Reishauer Dressage",
            "Pfauter 251",
            "Pfauter 630",
            "Pfauter 2300",
            "Modul 250x5",
            "Lidner",
            "Heckert ZFWVG 250",
            "Spiromatic",
        )
        self.cotasdemuda_cb.grid(row=2, column=1, sticky="ew")

        self.frames_map = {
            "Esferas": FrameEsferas,
            "Ek Roda Dentada": FrameRoda,
            "Ek Engrenagem": FrameEngrenagem,
            "Ek Sem-fim": FrameSemFim,
            "Rollete": FrameRollete,
            "Reishauer": FrameReishauer,
        }

        self.dimensoes_controlo_cb.bind("<<ComboboxSelected>>", self.on_ferramenta_selected)
        self.cotasdemuda_cb.bind("<<ComboboxSelected>>", self.on_cotasdemuda_selected)

    # Carrega a frame da ferramenta selecionada
    def on_ferramenta_selected(self, event):
        self.cotasdemuda_cb.set("")

        value = self.dimensoes_controlo_cb.get()
        frame_class = self.frames_map.get(value)

        if frame_class:
            self.load_callback(frame_class)

    def on_cotasdemuda_selected(self, event):
        self.dimensoes_controlo_cb.set("")

        value = self.cotasdemuda_cb.get()
        frame_class = self.frames_map.get(value)

        if frame_class:
            self.load_callback(frame_class)


if __name__ == "__main__":
    main()