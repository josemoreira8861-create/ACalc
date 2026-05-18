from math import cos, radians, sin, pi, atan, tan, acos, fabs
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

        self.entre_eixo = self.modulo*self.z1/cos(self.beta)

        # Se DENTRO do entre-eixo de funcionamento (x1 = 0)
        if self.entre_eixo == self.d1:
            self.d_a = self.d1+2*self.modulo
            self.x1 = 0

        # Se FORA do entre-eixo de funcionamento (x1 <> 0)
        else:
            self.valor_acos = ((self.entre_eixo) / self.d1) * cos(self.alpha_ap)
            self.entre_eixo_lim = self.entre_eixo * cos(self.alpha_ap)

            if self.valor_acos > 1:
                raise Exception(
                    f"O entre-eixo de funcionamento mínimo é "
                    f"{self.entre_eixo_lim:.3f} mm."
                )
            
            self.alpha_ap_func = acos(self.valor_acos)
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
        self.desvio_eff = self.x1 + ((self.Esm*(10**-3))/(2*self.modulo*tan(self.alpha)))

        self.Wk = (
            self.modulo * cos(self.alpha)
            * (
                pi * (self.k_dentes - 0.5)
                + self.z1 * self.inv_alpha_ap
            )
            + 2 * self.desvio_eff * self.modulo * sin(self.alpha)
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

# ----------------------- Wk Engrenagem -----------------------
class Engrenagem:
    def __init__(self, data):
        self.artigo = data["artigo"]
        self.allowance_series = data["allowance_series"]
        self.tolerance_series = data["tolerance_series"]
        self.tipo_dentado = data["tipo"]
        self.direcao_dentado = data["direcao"]
        self.a = data["entre eixo"]
        self.k_dentes_pinhao = round(data["k dentes pinhao"])
        self.k_dentes_roda = round(data["k dentes roda"])
        self.beta =  radians(data["angulo de helice"])
        self.alpha = radians(data["angulo de pressao"])
        self.modulo = data["modulo"]
        self.z1 = data["numero de dentes pinhao"]
        self.z2 = data["numero de dentes roda"]
        self.b = data["largura do dentado"]

        if self.tipo_dentado == "Reto":
            self.beta = 0
        
        if self.a == 0:
            self.a = self.modulo*(self.z1 + self.z2)/(cos(self.beta) * 2)

    def correcao(self):
        self.zv1 = self.z1/(cos(self.beta)**3)
        self.zv2 = self.z2/(cos(self.beta)**3)
        self.alpha_ap = atan(tan(self.alpha)/cos(self.beta))
        self.inv_alpha_ap = tan(self.alpha_ap) - self.alpha_ap
        self.d1 = (self.z1 * self.modulo) / cos(self.beta)
        self.d2 = (self.z2 * self.modulo) / cos(self.beta)

        self.entre_eixo = self.modulo*(self.z1 + self.z2)/(cos(self.beta) * 2)

        # Se DENTRO do entre-eixo de funcionamento (x1 + x2 = 0)
        if self.entre_eixo == self.a:
            self.d_a1 = self.d1 + 2*self.modulo
            self.d_a2 = self.d2 + 2*self.modulo
            self.x1 = 0
            self.x2 = 0

        # Se FORA do entre-eixo de funcionamento (x1 + x2 <> 0)
        else:
            self.valor_acos = ((self.entre_eixo) / self.a) * cos(self.alpha_ap)
            self.entre_eixo_lim = self.entre_eixo * cos(self.alpha_ap)

            if self.valor_acos > 1:
                raise Exception(
                    f"O entre-eixo de funcionamento mínimo é "
                    f"{self.entre_eixo_lim:.3f} mm."
                )

            self.alpha_ap_func = acos(self.valor_acos)
            self.inv_alpha_ap_func = tan(self.alpha_ap_func) - self.alpha_ap_func # alpha normal ou aparente v-- aqui?
            self.sum_desvios = ((self.z1 + self.z2)*(self.inv_alpha_ap_func- self.inv_alpha_ap))/(tan(self.alpha) * 2)
            self.x1 = (self.sum_desvios*self.zv1)/(self.zv1 + self.zv2) + 0.5 * ((self.zv2 - self.zv1)/(self.zv2 + self.zv1))
            self.x2 = self.sum_desvios - self.x1

            # cálculo do diâmetro de addendum corrigido
            self.B = (2*self.sum_desvios)/(self.z1 + self.z2)
            self.Bv = cos(self.alpha_ap)/cos(self.alpha_ap_func) - 1
            self.K = ((self.z1 + self.z2)/2) * (self.B - self.Bv)
            self.d_a1 = self.modulo * (self.z1/cos(self.beta) + 2 + 2*self.x1 - 2*self.K)
            self.d_a2 = self.modulo * (self.z2/cos(self.beta) + 2 + 2*self.x2 - 2*self.K)

    # DIN 3960, DIN 3967 e ISO 2771
    def cota_sobre_k_dentes(self):

        if self.k_dentes_pinhao == 0:
            self.alpha_vt1 = acos((self.z1*cos(self.alpha_ap))/(self.z1 + 2 * self.x1 * cos(self.beta)))
            self.beta_base = tan(self.beta) * cos(self.alpha_ap)
            self.k_dentes_pinhao = round((self.z1/pi)*(tan(self.alpha_vt1)/(cos(self.beta_base)**2) \
                 - self.inv_alpha_ap - (2*self.x1)/self.z1 * tan(self.alpha)) + 1)
            if self.k_dentes_pinhao < 1.5:
                self.k_dentes_pinhao = 2
            
        if self.k_dentes_roda == 0:
            self.alpha_vt2 = acos((self.z2*cos(self.alpha_ap))/(self.z2 + 2 * self.x2 * cos(self.beta)))
            self.beta_base = tan(self.beta) * cos(self.alpha_ap)
            self.k_dentes_roda = round((self.z2/pi)*(tan(self.alpha_vt2)/(cos(self.beta_base)**2) \
                 - self.inv_alpha_ap - (2*self.x2)/self.z2 * tan(self.alpha)) + 1)
            if self.k_dentes_roda < 1.5:
                self.k_dentes_roda = 2

        self.Esm1 = 0.5*(self.Ess1 + self.Esi1)
        self.desvio_eff1 = self.x1 + ((self.Esm1*(10**-3))/(2*self.modulo*tan(self.alpha)))

        self.Esm2 = 0.5*(self.Ess2 + self.Esi2)
        self.desvio_eff2 = self.x2 + ((self.Esm2*(10**-3))/(2*self.modulo*tan(self.alpha)))

        self.Wk1 = (
            self.modulo * cos(self.alpha)
            * (
                pi * (self.k_dentes_pinhao - 0.5)
                + self.z1 * self.inv_alpha_ap
            )
            + 2 * self.desvio_eff1 * self.modulo * sin(self.alpha)
        )

        self.Wk2 = (
            self.modulo * cos(self.alpha)
            * (
                pi * (self.k_dentes_roda - 0.5)
                + self.z2 * self.inv_alpha_ap
            )
            + 2 * self.desvio_eff2 * self.modulo * sin(self.alpha)
        )

        self.Tw1 = self.Ts1 * cos(self.alpha) * 10**(-3)
        self.Wk1_final = f"{self.Wk1:.5f} ± {self.Tw1/2:.5f}"

        self.Tw2 = self.Ts2 * cos(self.alpha) * 10**(-3)
        self.Wk2_final = f"{self.Wk2:.5f} ± {self.Tw2/2:.5f}"

    def calculate(self):
        self.correcao()

        self.valores_backlash1 = backlash(
            self.d1,
            self.beta,
            self.alpha,
            self.allowance_series,
            self.tolerance_series,
        )

        self.Ess1 = self.valores_backlash1["Ess"]
        self.Ts1 = self.valores_backlash1["Ts"]
        self.Esi1 = self.valores_backlash1["Esi"]
        self.fa1 = self.valores_backlash1["fa"]
        self.jt1 = self.valores_backlash1["jt"]
        self.jn1 = self.valores_backlash1["jn"]

        self.valores_backlash2 = backlash(
            self.d2,
            self.beta,
            self.alpha,
            self.allowance_series,
            self.tolerance_series,
        )

        self.Ess2 = self.valores_backlash2["Ess"]
        self.Ts2 = self.valores_backlash2["Ts"]
        self.Esi2 = self.valores_backlash2["Esi"]
        self.fa2 = self.valores_backlash2["fa"]
        self.jt2 = self.valores_backlash2["jt"]
        self.jn2 = self.valores_backlash2["jn"]

        self.classe = f"{self.allowance_series}{self.tolerance_series}"

        if self.tipo_dentado == "Helicoidal":
            self.tipo_pinhao = f"{self.tipo_dentado} ({self.direcao_dentado})"
            if self.direcao_dentado == "Esquerda":
                self.tipo_roda = f"{self.tipo_dentado} (Direita)"
            else:
                self.tipo_roda = f"{self.tipo_dentado} (Esquerda)"
        else:
            self.tipo_pinhao = f"{self.tipo_dentado}"
            self.tipo_roda = self.tipo_pinhao

        self.cota_sobre_k_dentes()

        return {
            "pinhao": {
                "Artigo": self.artigo,
                "Classe": self.classe,
                "Tipo de dentado": self.tipo_pinhao,
                "Diâmetro primitivo, d (mm)": self.d1,
                "Fator de correção, x": self.x1,
                "Diâmetro exterior corrigido, dₐ (mm)": self.d_a1,
                "Tolerância, Tₛ (µm)": self.Ts1,
                "Folga circular entre dentes, jₜ (mm)": self.jt1,
                "Folga normal entre dentes, jₙ (mm)": self.jn1,
                "Nº de dentes do Eₖ": self.k_dentes_pinhao,
                "Tolerância, Tw (mm)": self.Tw1,
                "Eₖ (mm)": self.Wk1_final,
            },

            "roda": {
                "Artigo": self.artigo,
                "Classe": self.classe,
                "Tipo de dentado": self.tipo_roda,
                "Diâmetro primitivo, d₂ (mm)": self.d2,
                "Fator de correção, x₂": self.x2,
                "Diâmetro exterior corrigido, dₐ₂ (mm)": self.d_a2,
                "Tolerância, Tₛ (µm)": self.Ts2,
                "Folga circular entre dentes, jₜ (mm)": self.jt2,
                "Folga normal entre dentes, jₙ (mm)": self.jn2,
                "Nº de dentes do Eₖ": self.k_dentes_roda,
                "Tolerância, Tw (mm)": self.Tw2,
                "Eₖ (mm)": self.Wk2_final,
            }
        }

# Lista das classes para ser chamada na acalc.py
COTAS = {
    "esferas": Esferas,
    "roda": Roda,
    "engrenagem": Engrenagem,
}