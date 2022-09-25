from helpers.Helpers import Helpers
class Nave:

    def __init__(self, numero, color):
        self.numero = numero
        self.capacidad = 0
        self.recorrido = []
        self.enViaje = False
        self.color = color

    def getNumero(self):
        return self.numero

    def getCapacidad(self):
        return self.capacidad

    def getColor(self):
        return self.color

    def setCapacidad(self, valor):
        self.capacidad = valor

    def puedeRecolectarMasMateriales(self):
        if(self.capacidad <= 30): return True
        else: return False

    def getEnViaje(self):
        return self.enViaje

    def setViaje(self, valor):
        self.enViaje = valor
    
    def cambiarRecorrido(self, arbolSistema):
        self.recorrido = []
        self.recorrido = Helpers.generarRecorrido(self, arbolSistema)

    def getRecorrido(self):
        return self.recorrido

    def guardarAlmacenamiento(self):
        #! hacer
        pass