from math import cos, radians, fabs, sin
from itertools import groupby
from operator import itemgetter


class Rollete: # Modelo Runderland 5A-4C
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

    def calculate(self):
        return self.rodasdemuda()

    def rodasdemuda(self, erro=0.0001):
        rodas = self.conj_rodas
        n = len(rodas)

        results = []

        for i in range(n):
            A = rodas[i]
            for j in range(n):
                if j == i:
                    continue
                B = rodas[j]

                for k in range(n):
                    if k in (i, j):
                        continue
                    C = rodas[k]

                    for l in range(n):
                        if l in (i, j, k):
                            continue
                        D = rodas[l]

                        razaom = (A / B) * (C / D)
                        err = fabs(self.razao - razaom)

                        if err <= erro:
                            if self.limites(A, B, C, D):
                                results.append({
                                    "A": A,
                                    "B": B,
                                    "C": C,
                                    "D": D,
                                    "erro": err,
                                    "razaom": razaom
                                })

        # Remove instâncias repetidas
        keyfunc = lambda d: (d["A"], d["B"], d["C"], d["D"])
        results = sorted(results, key=keyfunc)
        results = [next(g[1]) for g in groupby(results, key=keyfunc)]

        # Organiza com erro ascendente
        results.sort(key=itemgetter("erro"))

        # Ficam apenas 12 resultados
        return results[:12]
    
class Reishauer: # Modelo Reishauer
    def __init__(self, data):
        self.artigo = data["artigo"]
        self.sentido = data["sentido"].upper()
        self.modulo = data["modulo"]
        self.beta = radians(data["beta"])

        self.razao = 11.6909*sin(self.beta)/self.modulo

        self._conj_rodas = (
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

        if self.sentido == "ESQUERDA":
            AB = A + B
            CD = C + D

            return (
                AB <= 190 and total <= 394 and
                (
                    (CD >= 90 and total >= 229) or
                    (AB >= 84 and total >= 264)
                )
            )

        elif self.sentido == "DIREITA":
            CD = C + D

            return (
                CD <= 193 and total <= 383 and
                CD >= 71 and total >= 153
            )

        return False

    def calculate(self):
        return self.rodasdemuda()

    def rodasdemuda(self, erro=0.0001):
        rodas = self._conj_rodas
        n = len(rodas)

        results = []

        for i in range(n):
            A = rodas[i]
            for j in range(n):
                if j == i:
                    continue
                B = rodas[j]

                for k in range(n):
                    if k in (i, j):
                        continue
                    C = rodas[k]

                    for l in range(n):
                        if l in (i, j, k):
                            continue
                        D = rodas[l]

                        razaom = (A / B) * (C / D)
                        err = fabs(self.razao - razaom)

                        if err <= erro and self.limites(A, B, C, D):
                            results.append({
                                "A": A,
                                "B": B,
                                "C": C,
                                "D": D,
                                "erro": err,
                                "razaom": razaom
                            })

        keyfunc = lambda d: (d["A"], d["B"], d["C"], d["D"])
        results = sorted(results, key=keyfunc)
        results = [next(g[1]) for g in groupby(results, key=keyfunc)]

        results.sort(key=itemgetter("erro"))

        return results[:12]

# Lista das classes para ser chamada na acalc.py
RODAS = {
    "rollete": Rollete,
    "reishauer": Reishauer,
}