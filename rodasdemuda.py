from math import cos, radians, fabs, sin
from itertools import groupby, permutations
from operator import itemgetter

class RodasDeMuda:
    def rodasdemuda(self, erro=0.0001):
        rodas = self.conj_rodas
        results = []

        for A, B, C, D in permutations(rodas, 4):

            if not self.limites(A, B, C, D):
                continue

            razaom = (A / B) * (C / D)
            err = fabs(self.razao - razaom)

            if err <= erro:
                results.append({
                    "A": A,
                    "B": B,
                    "C": C,
                    "D": D,
                    "erro": err,
                    "razaom": razaom
                })

        # Remove conjuntos de rodas repetidos
        keyfunc = lambda d: (d["A"], d["B"], d["C"], d["D"])
        results = sorted(results, key=keyfunc)
        results = [next(g[1]) for g in groupby(results, key=keyfunc)]

        # Organiza com erro ascendente
        results.sort(key=itemgetter("erro"))

        # Ficam apenas 12 resultados
        return results[:12]

    def calculate(self):
        return self.rodasdemuda()

class Rollete(RodasDeMuda): # Modelo Runderland 5A-4C
    def __init__(self, data):
        self.artigo = data["artigo"]
        self.modulo = data["modulo"]
        self.beta = radians(data["beta"])

        self.razao = self.modulo / (4.5 * cos(self.beta))

        self.conj_rodas = (
            27, 28, 30, 30, 32, 33, 35, 36, 38, 39, 40, 40, 40,
            42, 42, 44, 45, 46, 48, 48, 50, 51, 52, 53, 54, 55,
            56, 57, 58, 59, 60, 60, 60, 61, 62, 63, 64, 65, 67,
            68, 70, 71, 72, 73, 74, 75, 76, 79, 82, 83, 84, 86,
            89, 93, 94, 96, 97, 100, 105, 107, 108, 110, 120, 127
        )

    def limites(self, A, B, C, D):
        return (
            78 <= (A + B) <= 120 and
            88 <= (C + D) <= 135
        )

    # Esta função é chamada na acalc.py, apesar de parecer desnecessário ter esta função
    # nas rodas de muda (visto que usam todas a função rodasdemuda()), esta torna-se
    # útil nos cálculos das cotas de verificação que já irão usar funções diferentes,
    # assim, generaliza-se
    def calculate(self):
        return self.rodasdemuda()
    
class Reishauer(RodasDeMuda):
    def __init__(self, data):
        self.artigo = data["artigo"]
        self.sentido = data["sentido"]
        self.modulo = data["modulo"]
        self.beta = radians(data["beta"])

        self.razao = 11.6909*sin(self.beta)/self.modulo

        self.conj_rodas = (
            35,36,38,40,40,41,42,43,44,45,45,46,47,48,49,50,50,51,52,53,
            54,55,56,57,58,59,60,60,61,62,63,64,65,66,67,68,69,70,70,71,
            72,73,74,75,75,76,78,80,80,81,82,84,85,86,87,88,90,90,91,92,
            93,94,95,96,100,101,103,105,106,108,110,112,118,120
        )
    
    def limites(self, A, B, C, D):
        total = A + B + C + D

        # Basic constraints
        if not (
            A <= 105 and
            B <= (C + D - 34) and
            C <= (A + B - 23) and
            D <= 120
        ):
            return False

        if self.sentido == "Esquerda":
            AB = A + B
            CD = C + D

            return (
                AB <= 190 and total <= 394 and
                (
                    (CD >= 90 and total >= 229) or
                    (AB >= 84 and total >= 264)
                )
            )

        elif self.sentido == "Direita":
            CD = C + D

            return (
                CD <= 193 and total <= 383 and
                CD >= 71 and total >= 153
            )

        return False

    def calculate(self):
        return self.rodasdemuda()
    
class ReishauerDressage(RodasDeMuda):
    def __init__(self, data):
        self.artigo = data["artigo"]
        self.modulo = data["modulo"]

        self.razao = 6/25.4*self.modulo

        self.conj_rodas = (
            35,36,38,40,40,41,42,43,44,45,45,46,47,48,49,50,50,51,
            52,53,54,55,56,57,58,59,60,60,61,62,63,64,65,66,67,68,
            69,70,70,71,72,73,74,75,75,76,78,80,80,81,82,84,85,86,
            87,88,90,90,91,92,93,94,95,96,100,101,103,105,106,108,
            110,112,118,120)
        
    def limites(self, A, B, C, D):
        AB = A + B
        CD = C + D
        total = AB + CD

        return (
            A <= 60 and
            B <= (CD - 34) and
            C <= (AB - 23) and
            D <= 105 and
            AB <= 166 and
            CD <= 145 and
            total <= 311 and
            (
                (CD >= 108 and total >= 216) or
                (AB >= 84 and total >= 229)
            )
        )

    def calculate(self):
        return self.rodasdemuda()

class Pfauter251(RodasDeMuda):
    def __init__(self, data):
        self.artigo = data["artigo"]
        self.modo = data["modo"]
        self.modulo = data["modulo"]
        self.beta = radians(data["beta"])
        self.num_entradas = data["num_entradas"]

        if self.modo == "Diferencial":
            self.razao = (2.864789*sin(self.beta))/(self.modulo*self.num_entradas)
        elif self.modo == "Tangencial" or "Navalhão":
            self.razao = (3*cos(self.beta))/(2*self.modulo*self.num_entradas)
        else:
            self.razao = None

        self.conj_rodas = (
            20,21,22,23,24,24,25,25,26,27,27,28,29,29,30,31,32,32,
            33,34,35,36,36,37,38,38,39,40,40,41,42,42,43,44,45,45,
            46,47,48,48,49,50,51,52,53,54,55,56,57,58,58,59,60,60,
            61,62,63,64,64,65,66,67,68,69,70,71,71,72,72,73,74,75,
            76,77,78,79,80,81,82,83,84,86,87,88,89,92,94,95,96,97,
            98,101,102,103,107,109,113,127)

    
    def limites(self, A, B, C, D):
        AB = A + B
        CD = C + D
        min_CD = B+21 if B>=39 else 60 

        return (
            80 <= AB <= 170 and
            min_CD <= CD <= 180 and
            D <= 127
        )
    
    def calculate(self):
        return self.rodasdemuda()


# Lista das classes para ser chamada na acalc.py
RODAS = {
    "rollete": Rollete,
    "reishauer": Reishauer,
    "reishauer_dressage": ReishauerDressage,
    "pfauter251": Pfauter251,
}