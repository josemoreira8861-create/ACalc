class Esferas:
    def __init__(self, data):
        self.diameter = data["diameter"]
        self.type = data["type"]

    def calculate(self):
        if self.type == "Option1":
            return self.diameter * 2
        return self.diameter * 3


# Lista das classes para ser chamada na app.py
COTAS = {
    "esferas": Esferas,
}