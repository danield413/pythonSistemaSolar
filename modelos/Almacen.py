class Almacen:

    def __init__(self):
        self.oro = 0
        self.plata = 0
        self.bronce = 0

    def getOroAlmacenado(self):
        return self.oro

    def getPlataAlmacenada(self):
        return self.plata

    def getBronceAlmacenado(self):
        return self.bronce

    def setOroAlmacenado(self, valor):
        self.oro = valor

    def setPlataAlmacenada(self, valor):
        self.plata = valor

    def setBronceAlmacenado(self, valor):
        self.bronce = valor