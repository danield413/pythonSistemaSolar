import time


class Saludo:

    def __init__(self, m) -> None:
        self.m = m

    def saludar(self, nombreHilo, componenteGrafico):
        for i in range(10):
            time.sleep(1)
            print("Hola mundo cruel :( {0}".format(self.m))
            componenteGrafico.insert("1.0", "Hola mundo cruel "+ str(self.m) + "\n")