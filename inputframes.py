import tkinter as tk
from tkinter import ttk


class BaseToolFrame(ttk.Frame):
    def __init__(self, parent, tool_name, on_calculate):
        super().__init__(parent)

        self.tool_name = tool_name
        self.on_calculate = on_calculate


# ---------------- ESFERAS ----------------
class FrameEsferas(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "esferas", on_calculate)

        self.diameter_var = tk.DoubleVar()
        self.type_var = tk.StringVar()

        ttk.Label(self, text="Type").grid(row=0, column=0)
        ttk.Combobox(self, textvariable=self.type_var,
                     values=["Option1", "Option2"]).grid(row=0, column=1)

        ttk.Label(self, text="Diameter").grid(row=1, column=0)
        ttk.Entry(self, textvariable=self.diameter_var).grid(row=1, column=1)

        ttk.Button(self, text="Calculate", command=self.send_data)\
            .grid(row=2, column=0, columnspan=2)


    def send_data(self):
        self.on_calculate(self.tool_name, {
            "diameter": self.diameter_var.get(),
            "type": self.type_var.get(),
        })


# ---------------- ROLLETE ----------------
class FrameRollete(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "rollete", on_calculate)

        self.artigo = tk.StringVar()
        self.modulo = tk.DoubleVar()
        self.beta = tk.DoubleVar()

        ttk.Label(self, text="Artigo").grid(row=0, column=0)
        ttk.Entry(self, textvariable=self.artigo).grid(row=0, column=1)

        ttk.Label(self, text="Modulo").grid(row=1, column=0)
        ttk.Entry(self, textvariable=self.modulo).grid(row=1, column=1)

        ttk.Label(self, text="Beta").grid(row=2, column=0)
        ttk.Entry(self, textvariable=self.beta).grid(row=2, column=1)

        ttk.Button(self, text="Calculate", command=self.send_data)\
            .grid(row=3, column=0, columnspan=2)

    def send_data(self):
        self.on_calculate(self.tool_name, {
            "artigo": self.artigo.get(),
            "modulo": self.modulo.get(),
            "beta": self.beta.get(),
        })

# ---------------- REISHAUER ------------------
class FrameReishauer(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "reishauer", on_calculate)
        
        self.artigo = tk.StringVar()
        self.sentido = tk.StringVar()
        self.modulo = tk.DoubleVar()
        self.beta = tk.DoubleVar()

        ttk.Label(self, text="Artigo").grid(row=0, column=0)
        ttk.Entry(self, textvariable=self.artigo).grid(row=0, column=1)

        ttk.Label(self, text="Sentido").grid(row=1, column=0)
        ttk.Combobox(self, textvariable=self.sentido,
                     values=["Esquerda", "Direita"]).grid(row=1, column=1)

        ttk.Label(self, text="Modulo").grid(row=2, column=0)
        ttk.Entry(self, textvariable=self.modulo).grid(row=2, column=1)

        ttk.Label(self, text="Beta").grid(row=3, column=0)
        ttk.Entry(self, textvariable=self.beta).grid(row=3, column=1)

        ttk.Button(self, text="Calculate", command=self.send_data)\
            .grid(row=4, column=0, columnspan=2)

    def send_data(self):
        self.on_calculate(self.tool_name, {
            "artigo": self.artigo.get(),
            "sentido": self.sentido.get(),
            "modulo": self.modulo.get(),
            "beta": self.beta.get(),
        })


# ---------------- PLACEHOLDERS ----------------
class FrameRoda(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "roda", on_calculate)
        ttk.Label(self, text="Roda Dentada").grid()


class FrameEngrenagem(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "engrenagem", on_calculate)
        ttk.Label(self, text="Engrenagem").grid()


class FrameSemFim(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "semfim", on_calculate)
        ttk.Label(self, text="Sem-fim").grid()