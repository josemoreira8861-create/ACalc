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
        ttk.Label(self, text="Cota diametral sobre esferas").grid(row=0, column=0, columnspan=2)

        self.diameter_var = tk.DoubleVar()
        self.type_var = tk.StringVar()

        ttk.Label(self, text="Type").grid(row=1, column=0)
        ttk.Combobox(self, textvariable=self.type_var,
                     values=["Option1", "Option2"]).grid(row=1, column=1)

        ttk.Label(self, text="Diameter").grid(row=2, column=0)
        ttk.Entry(self, textvariable=self.diameter_var).grid(row=2, column=1)

        ttk.Button(self, text="Calcular", command=self.send_data)\
            .grid(row=3, column=0, columnspan=2)


    def send_data(self):
        self.on_calculate(self.tool_name, {
            "diameter": self.diameter_var.get(),
            "type": self.type_var.get(),
        })


# ---------------- ROLLETE ----------------
class FrameRollete(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "rollete", on_calculate)
        ttk.Label(self, text="Rollete").grid(row=0, column=0, columnspan=2)

        self.artigo = tk.StringVar()
        self.modulo = tk.DoubleVar()
        self.beta = tk.DoubleVar()

        ttk.Label(self, text="Artigo").grid(row=1, column=0)
        ttk.Entry(self, textvariable=self.artigo).grid(row=1, column=1)

        ttk.Label(self, text="Módulo").grid(row=2, column=0)
        ttk.Entry(self, textvariable=self.modulo).grid(row=2, column=1)

        ttk.Label(self, text="Beta (graus)").grid(row=3, column=0)
        ttk.Entry(self, textvariable=self.beta).grid(row=3, column=1)

        ttk.Button(self, text="Calcular", command=self.send_data)\
            .grid(row=4, column=0, columnspan=2)

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
        ttk.Label(self, text="Reishauer").grid(row=0, column=0, columnspan=2)
        
        self.artigo = tk.StringVar()
        self.sentido = tk.StringVar()
        self.modulo = tk.DoubleVar()
        self.beta = tk.DoubleVar()

        ttk.Label(self, text="Artigo").grid(row=1, column=0)
        ttk.Entry(self, textvariable=self.artigo).grid(row=1, column=1)

        ttk.Label(self, text="Sentido").grid(row=2, column=0)
        ttk.Combobox(self, state="readonly", textvariable=self.sentido,
                     values=["Esquerda", "Direita"]).grid(row=2, column=1)

        ttk.Label(self, text="Módulo").grid(row=3, column=0)
        ttk.Entry(self, textvariable=self.modulo).grid(row=3, column=1)

        ttk.Label(self, text="Beta (graus)").grid(row=4, column=0)
        ttk.Entry(self, textvariable=self.beta).grid(row=4, column=1)

        ttk.Button(self, text="Calcular", command=self.send_data)\
            .grid(row=5, column=0, columnspan=2)

    def send_data(self):
        self.on_calculate(self.tool_name, {
            "artigo": self.artigo.get(),
            "sentido": self.sentido.get(),
            "modulo": self.modulo.get(),
            "beta": self.beta.get(),
        })

class FrameReishauerDressage(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "reishauer_dressage", on_calculate)
        ttk.Label(self, text="Reishauer Dressage").grid(row=0, column=0, columnspan=2)

        self.artigo = tk.StringVar()
        self.modulo = tk.DoubleVar()

        ttk.Label(self, text="Artigo").grid(row=1, column=0)
        ttk.Entry(self, textvariable=self.artigo).grid(row=1, column=1)

        ttk.Label(self, text="Módulo").grid(row=2, column=0)
        ttk.Entry(self, textvariable=self.modulo).grid(row=2, column=1)

        ttk.Button(self, text="Calcular", command=self.send_data)\
            .grid(row=3, column=0, columnspan=2)

    def send_data(self):
        self.on_calculate(self.tool_name, {
            "artigo": self.artigo.get(),

            "modulo": self.modulo.get(),
        })

# ------------------------- PFAUTER & MODUL ------------------------
class FramePfauter(BaseToolFrame):
    def __init__(self, parent, on_calculate, tool_name, title):
        super().__init__(parent, tool_name, on_calculate)
        ttk.Label(self, text=title).grid(row=0, column=0, columnspan=2)
        
        self.artigo = tk.StringVar()
        self.modo = tk.StringVar()
        self.modulo = tk.DoubleVar()
        self.beta = tk.DoubleVar()
        self.num_entradas = tk.IntVar()

        ttk.Label(self, text="Artigo").grid(row=1, column=0)
        ttk.Entry(self, textvariable=self.artigo).grid(row=1, column=1)

        ttk.Label(self, text="Modo").grid(row=2, column=0)
        ttk.Combobox(self, state="readonly", textvariable=self.modo,
                     values=["Diferencial", "Tangencial", "Navalhão"]).grid(row=2, column=1)

        ttk.Label(self, text="Módulo (Mn)").grid(row=3, column=0)
        ttk.Entry(self, textvariable=self.modulo).grid(row=3, column=1)

        ttk.Label(self, text="Beta (graus)").grid(row=4, column=0)
        ttk.Entry(self, textvariable=self.beta).grid(row=4, column=1)

        ttk.Label(self, text="Nº de entradas").grid(row=5, column=0)
        ttk.Entry(self, textvariable=self.num_entradas).grid(row=5, column=1)

        ttk.Button(self, text="Calcular", command=self.send_data)\
            .grid(row=6, column=0, columnspan=2)

    def send_data(self):
        self.on_calculate(self.tool_name, {
            "artigo": self.artigo.get(),
            "modo": self.modo.get(),
            "modulo": self.modulo.get(),
            "beta": self.beta.get(),
            "num_entradas": self.num_entradas.get(),
        })

# ----------------------- LINDNER & HECKERT -----------------------
class FrameLindner(BaseToolFrame):
    def __init__(self, parent, on_calculate, tool_name, title):
        super().__init__(parent, tool_name, on_calculate)
        ttk.Label(self, text=title).grid(row=0, column=0, columnspan=2)

        self.artigo = tk.StringVar()
        self.modulo_axial = tk.DoubleVar()
        self.num_entradas = tk.IntVar()

        ttk.Label(self, text="Artigo").grid(row=1, column=0)
        ttk.Entry(self, textvariable=self.artigo).grid(row=1, column=1)

        ttk.Label(self, text="Módulo axial").grid(row=2, column=0)
        ttk.Entry(self, textvariable=self.modulo_axial).grid(row=2, column=1)

        ttk.Label(self, text="Nº de entradas").grid(row=3, column=0)
        ttk.Entry(self, textvariable=self.num_entradas).grid(row=3, column=1)

        ttk.Button(self, text="Calcular", command=self.send_data)\
            .grid(row=4, column=0, columnspan=2)

    def send_data(self):
        self.on_calculate(self.tool_name, {
            "artigo": self.artigo.get(),
            "modulo_axial": self.modulo_axial.get(),
            "num_entradas": self.num_entradas.get(),
        })

# ---------------- RODA DENTADA ----------------
class FrameRoda(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "roda", on_calculate)
        ttk.Label(self, text="Ek Roda Dentada").grid(row=0, column=0, columnspan=2)

        self.artigo = tk.StringVar()
        self.tipo_dentado = tk.StringVar()
        self.direcao_dentado = tk.StringVar()
        self.d1 = tk.DoubleVar()
        self.k_dentes = tk.IntVar()
        self.beta = tk.DoubleVar()
        self.alpha = tk.DoubleVar()
        self.modulo = tk.DoubleVar()
        self.z1 = tk.IntVar()
        self.b = tk.DoubleVar()

        ttk.Label(self, text="Artigo").grid(row=1, column=0)
        ttk.Entry(self, textvariable=self.artigo).grid(row=1, column=1)

        ttk.Label(self, text="Tipo de dentado").grid(row=2, column=0)
        ttk.Combobox(self, state="readonly", textvariable=self.tipo_dentado,
                     values=["Helicoidal", "Reto"]).grid(row=2, column=1)
        
        ttk.Label(self, text="Direção do dentado").grid(row=3, column=0)
        ttk.Combobox(self, state="readonly", textvariable=self.direcao_dentado,
                     values=["Esquerda", "Direita"]).grid(row=3, column=1)
        
        ttk.Label(self, text="Diâmetro primitivo (0 = Auto)").grid(row=4, column=0)
        ttk.Entry(self, textvariable=self.d1).grid(row=4, column=1)

        ttk.Label(self, text="Nº de dentes do Ek (0 = Auto)").grid(row=5, column=0)
        ttk.Entry(self, textvariable=self.k_dentes).grid(row=5, column=1)

        ttk.Label(self, text="Ângulo de hélice (graus)").grid(row=6, column=0)
        ttk.Entry(self, textvariable=self.beta).grid(row=6, column=1)

        ttk.Label(self, text="Ângulo de pressão (graus)").grid(row=7, column=0)
        ttk.Entry(self, textvariable=self.alpha).grid(row=7, column=1)

        ttk.Label(self, text="Módulo").grid(row=8, column=0)
        ttk.Entry(self, textvariable=self.modulo).grid(row=8, column=1)

        ttk.Label(self, text="Nº de dentes").grid(row=9, column=0)
        ttk.Entry(self, textvariable=self.z1).grid(row=9, column=1)

        ttk.Label(self, text="Largura do dentado").grid(row=10, column=0)
        ttk.Entry(self, textvariable=self.b).grid(row=10, column=1)

        ttk.Button(self, text="Calcular", command=self.send_data)\
            .grid(row=11, column=0, columnspan=2)
        
    def send_data(self):
          self.on_calculate(self.tool_name, {
            "artigo": self.artigo.get(),
            "tipo": self.tipo_dentado.get(),
            "direcao": self.direcao_dentado.get(),
            "diametro primitivo": self.d1.get(),
            "k dentes": self.k_dentes.get(),
            "angulo de helice": self.beta.get(),
            "angulo de pressao": self.alpha.get(),
            "modulo": self.modulo.get(),
            "numero de dentes": self.z1.get(),
            "largura do dentado": self.b.get(),
        })

# ---------------- PLACEHOLDERS ----------------
class FrameEngrenagem(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "engrenagem", on_calculate)
        ttk.Label(self, text="Engrenagem").grid()


class FrameSemFim(BaseToolFrame):
    def __init__(self, parent, on_calculate):
        super().__init__(parent, "semfim", on_calculate)
        ttk.Label(self, text="Sem-fim").grid()