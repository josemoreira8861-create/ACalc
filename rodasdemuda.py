from math import cos, radians, fabs
from itertools import groupby
from operator import itemgetter


class Rollete:
    def __init__(self, data):
        self.artigo = data["artigo"]
        self.modulo = data["modulo"]
        self.beta = radians(data["beta"])

        self.razao = self.modulo / (4.5 * cos(self.beta))

        self.name = "rollete"
        self.modelo = "Runderland 5A-4C"

        self.conj_rodas = (
            27, 28, 30, 30, 32, 33, 35, 36, 38, 39, 40, 40, 40,
            42, 42, 44, 45, 46, 48, 48, 50, 51, 52, 53, 54, 55,
            56, 57, 58, 59, 60, 60, 60, 61, 62, 63, 64, 65, 67,
            68, 70, 71, 72, 73, 74, 75, 76, 79, 82, 83, 84, 86,
            89, 93, 94, 96, 97, 100, 105, 107, 108, 110, 120, 127
        )

    # ---------------- LIMIT CHECK ----------------
    def limites(self, A, B, C, D):
        return (
            78 <= (A + B) <= 120 and
            88 <= (C + D) <= 135
        )

    def calculate(self):
        return self.rodasdemuda()

    # ---------------- MAIN SEARCH ----------------
    def rodasdemuda(self, erro=0.001):
        rodas = self.conj_rodas
        n = len(rodas)

        results = []

        for i in range(n):
            A = rodas[i]
            for j in range(n):
                B = rodas[j]
                if j == i:
                    continue

                for k in range(n):
                    C = rodas[k]
                    if k in (i, j):
                        continue

                    for l in range(n):
                        D = rodas[l]
                        if l in (i, j, k):
                            continue

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

        # REMOVE DUPLICATES
        keyfunc = lambda d: (d["A"], d["B"], d["C"], d["D"])
        results = sorted(results, key=keyfunc)
        results = [next(g[1]) for g in groupby(results, key=keyfunc)]

        # SORT
        results.sort(key=itemgetter("erro"))

        return results  

# Lista das classes para ser chamada na app.py
RODAS = {
    "rollete": Rollete,
}