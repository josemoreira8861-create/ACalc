from math import cos, radians, sin, pi, atan, tan, acos
from din3967_tables import ALLOWANCE_SERIES, TOLERANCE_SERIES

# ----------------------- Função para o backlash -----------------------
# DIN 3960, DIN 3961 e DIN 3967
def backlash(d1, beta, alpha, allowance_series, tolerance_series):

    serie_allowance = ALLOWANCE_SERIES[allowance_series]
    serie_tolerance = TOLERANCE_SERIES[tolerance_series]

    Ess = None
    Ts = None

    for lower, upper, value in serie_allowance:
        if lower < d1 <= upper:
            Ess = value
            break

    for lower, upper, value in serie_tolerance:
        if lower < d1 <= upper:
            Ts = value
            break

    Esi = Ess - Ts
    fa = Ess

    # circumferential backlash
    jt = (
        0
        - 2 * Ess / cos(beta)
        + 2 * fa * tan(alpha) / cos(beta)
    ) * 10**(-3)

    # normal backlash
    jn = jt * cos(alpha) * cos(beta)

    return {
        "Ess": Ess,
        "Ts": Ts,
        "Esi": Esi,
        "fa": fa,
        "jt": jt,
        "jn": jn,
    }

# ----------------------- Esferas -----------------------
class Esferas:
    def __init__(self, data):
        self.diameter = data["diameter"]
        self.type = data["type"]

    def calculate(self):
        if self.type == "Option1":
            return self.diameter * 2
        return self.diameter * 3

# ----------------------- Wk Roda Dentada -----------------------
class Roda:
    def __init__(self, data):
        self.artigo = data["artigo"]
        self.allowance_series = data["allowance_series"]
        self.tolerance_series = data["tolerance_series"]
        self.tipo_dentado = data["tipo"]
        self.direcao_dentado = data["direcao"]
        self.d1 = data["diametro primitivo"]
        self.k_dentes = round(data["k dentes"])
        self.beta =  radians(data["angulo de helice"])
        self.alpha = radians(data["angulo de pressao"])
        self.modulo = data["modulo"]
        self.z1 = data["numero de dentes"]
        self.b = data["largura do dentado"]

        if self.tipo_dentado == "Reto":
            self.beta = 0
        
        if self.d1 == 0:
            self.d1 = self.modulo*self.z1/cos(self.beta)

    def correcao(self):
        self.zv = self.z1/(cos(self.beta)**3)
        self.alpha_ap = atan(tan(self.alpha)/cos(self.beta))
        self.inv_alpha_ap = tan(self.alpha_ap) - self.alpha_ap

        self.entre_eixo = 2*(self.modulo*self.z1/cos(self.beta))

        # Se DENTRO do entre-eixo de funcionamento (x1 = 0)
        if self.entre_eixo == 2*self.d1:
            self.d_a = self.d1+2*self.modulo
            self.x1 = 0

        # Se FORA do entre-eixo de funcionamento (x1 <> 0)
        else:
            self.alpha_ap_func = acos(((self.entre_eixo/2)/self.d1)*cos(self.alpha_ap))
            self.inv_alpha_ap_func = tan(self.alpha_ap_func) - self.alpha_ap_func
            self.sum_desvios = (self.z1*(self.inv_alpha_ap_func- self.inv_alpha_ap))/tan(self.alpha)
            self.x1 = (self.sum_desvios*self.zv)/(2*self.zv)

            # cálculo do diâmetro de addendum corrigido
            self.B = (2*self.sum_desvios)/(2*self.z1)
            self.Bv = cos(self.alpha_ap)/cos(self.alpha_ap_func) - 1
            self.K = self.z1*(self.B - self.Bv)
            self.d_a = self.modulo * (self.z1/cos(self.beta) + 2 + 2*self.x1 - 2*self.K)

    # DIN 3960, DIN 3967 e ISO 2771
    def cota_sobre_k_dentes(self):

        if self.k_dentes == 0:
            self.alpha_vt = acos((self.z1*cos(self.alpha_ap))/(self.z1 + 2 * self.x1 * cos(self.beta)))
            self.beta_base = tan(self.beta) * cos(self.alpha_ap)
            self.k_dentes = round((self.z1/pi)*(tan(self.alpha_vt)/(cos(self.beta_base)**2) \
                 - self.inv_alpha_ap - (2*self.x1)/self.z1 * tan(self.alpha)) + 1)
            if self.k_dentes < 1.5:
                self.k_dentes = 2

        self.Esm = 0.5*(self.Ess + self.Esi)
        self.desvio_eff = self.x1 + (self.Esm/(2*self.modulo*tan(self.alpha)))

        self.Wk = (
            self.modulo * cos(self.alpha)
            * (
                pi * (self.k_dentes - 0.5)
                + self.z1 * self.inv_alpha_ap
            )
            + 2 * self.x1 * self.modulo * sin(self.alpha)
        )

        self.Tw = self.Ts * cos(self.alpha) * 10**(-3)

        self.Wk_final = f"{self.Wk:.5f} ± {self.Tw/2:.5f}"

    def calculate(self):
        self.correcao()

        self.valores_backlash = backlash(
            self.d1,
            self.beta,
            self.alpha,
            self.allowance_series,
            self.tolerance_series,
        )

        self.Ess = self.valores_backlash["Ess"]
        self.Ts = self.valores_backlash["Ts"]
        self.Esi = self.valores_backlash["Esi"]
        self.fa = self.valores_backlash["fa"]
        self.jt = self.valores_backlash["jt"]
        self.jn = self.valores_backlash["jn"]

        self.classe = f"{self.allowance_series}{self.tolerance_series}"

        if self.tipo_dentado == "Helicoidal":
            self.tipo = f"{self.tipo_dentado} ({self.direcao_dentado})"
        else:
            self.tipo = f"{self.tipo_dentado}"

        self.cota_sobre_k_dentes()

        return {
            "Artigo": self.artigo,
            "Classe": self.classe,
            "Tipo de dentado": self.tipo,
            "Diâmetro primitivo, d₁ (mm)": self.d1,
            "Fator de correção, x₁": self.x1,
            "Diâmetro exterior corrigido, dₐ (mm)": self.d_a,
            "Tolerância, Tₛ (pm)": self.Ts,
            "Folga circular entre dentes, jₜ (mm)": self.jt,
            "Folga normal entre dentes, jₙ (mm)": self.jn,
            "Nº de dentes do Eₖ": self.k_dentes,
            "Tolerância, Tw (mm)": self.Tw,
            "Eₖ (mm)": self.Wk_final,
        }


# Lista das classes para ser chamada na acalc.py
COTAS = {
    "esferas": Esferas,
    "roda": Roda,
}