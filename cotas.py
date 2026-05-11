from math import cos, radians, fabs, sin, pi, atan, tan, acos

class Esferas:
    def __init__(self, data):
        self.diameter = data["diameter"]
        self.type = data["type"]

    def calculate(self):
        if self.type == "Option1":
            return self.diameter * 2
        return self.diameter * 3

class Roda:
    def __init__(self, data):
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
    
    def backlash(self):

        serie_cd = [
            (0, 10, -40), (10, 50, -54),
            (50, 125, -70),(125, 280, -95), 
            (280, 560, -130),(560, 1000, -175), 
            (1000, 1600, -240),(1600, 2500, -320), 
            (2500, 4000, -430),(4000, 6300, -580), 
            (6300, 10000, -780),
            ]
        
        for lower, upper, value in serie_cd:
            if lower < self.d1 <= upper:
                self.Ess = value
        
        serie_25 = [
            (0, 10, 20),(10, 50, 30), 
            (50, 125, 40),(125, 280, 50), 
            (280, 560, 60),(560, 1000, 80), 
            (1000, 1600, 100),(1600, 2500, 130), 
            (2500, 4000, 160),(4000, 6300, 200), 
            (6300, 10000, 250),
            ]
        
        for lower, upper, value in serie_25:
            if lower < self.d1 <= upper:
                self.Ts = value
        
        self.Esi = self.Ess - self.Ts
        self.fa = self.Ess

        # circumferential backlash
        self.jt = 0 - 2*self.Ess/cos(self.beta) + 2*self.fa * tan(self.alpha)/cos(self.beta)

        # normal backlash
        self.jn = self.jt * cos(self.alpha) * cos(self.beta)

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

        self.Wk_final = f"{self.Wk:.4f} ± {self.Tw/2:.4f}"

# Lista das classes para ser chamada na acalc.py
COTAS = {
    "esferas": Esferas,
}