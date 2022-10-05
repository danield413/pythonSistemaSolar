from helpers.Helpers import Helpers
class Nave:

    def __init__(self, numero):
        self.numero = numero
        self.capacidadOro = 0
        self.capacidadPlata = 0
        self.capacidadBronce = 0
        self.recorrido = []
        self.enViaje = False
        self.cargaLlena = False

    def getCargaLlena(self):
        return self.cargaLlena

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

    def getEnViaje(self):
        return self.enViaje

    def setViaje(self, valor):
        self.enViaje = valor

    def setCapacidadOro(self, valor):
        self.capacidadOro = valor

    def setCapacidadPlata(self, valor):
        self.capacidadPlata = valor

    def setCapacidadBronce(self, valor):
        self.capacidadBronce = valor

    def setCargaLlena(self, valor):
        self.cargaLlena = valor

    def getRecorrido(self):
        return self.recorrido

    def resetRecorrido(self):
        self.recorrido = []

    def cambiarRecorrido(self, arbolSistema):
        self.recorrido = []
        self.recorrido = Helpers.generarRecorrido(self, arbolSistema)
        return self.recorrido

