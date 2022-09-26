from helpers.Helpers import Helpers
class Nave:

    def __init__(self, numero, color):
        self.numero = numero
        self.capacidad = 0
        self.capacidadOro = 0
        self.capacidadPlata = 0
        self.capacidadBronce = 0
        self.recorrido = []
        self.enViaje = False
        self.color = color
        self.cargaLlena = False

    def getCargaLlena(self):
        return self.cargaLlena

    def setCargaLlena(self, valor):
        self.cargaLlena = valor

    def getNumero(self):
        return self.numero

    def getCapacidad(self):
        return self.capacidad

    def getCapacidadOro(self):
        return self.capacidadOro

    def getCapacidadPlata(self):
        return self.capacidadPlata

    def getCapacidadBronce(self):
        return self.capacidadBronce

    def getColor(self):
        return self.color

    def setCapacidad(self, valor):
        self.capacidad = valor

    def setCapacidadOro(self, valor):
        self.capacidadOro = valor

    def setCapacidadPlata(self, valor):
        self.capacidadPlata = valor

    def setCapacidadBronce(self, valor):
        self.capacidadBronce = valor

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