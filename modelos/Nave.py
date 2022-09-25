class Nave:

    def __init__(self, numero):
        self.numero = numero
        self.capacidad = 0
        self.planetasVisitados = []
        self.enViaje = False

    def getNumero(self):
        return self.numero

    def getCapacidad(self):
        return self.capacidad

    def setCapacidad(self, valor):
        self.capacidad = valor

    def puedeRecolectarMasMateriales(self):
        if(self.capacidad <= 30): return True
        else: return False

    def getEnViaje(self):
        return self.enViaje

    def setViaje(self, valor):
        self.enViaje = valor
    