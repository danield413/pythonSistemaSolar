class MaterialNodo:

    def __init__(self, codigo, fecha, tipoMaterial, cantidad):
        self.izquierda = None
        self.derecha = None
        self.codigo = codigo
        self.fecha = fecha
        self.tipoMaterial = tipoMaterial
        self.cantidad = cantidad
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.color = "white"
        self.textX = 0
        self.textColor = "white"

    def getTextColor(self):
        return self.textColor

    def setTextColor(self, valor):
        self.textColor = valor

    def getTextX(self):
        return self.textX

    def setTextX(self, valor):
        self.textX = valor

    def getColor(self):
        return self.color

    def setColor(self, valor):
        self.color = valor        
    
    def getX(self):
        return self.x1

    def getY(self):
        return self.y1

    def getX2(self):
        return self.x2

    def getY2(self):
        return self.y2

    def setX(self, valor):
        self.x1 = valor

    def setY(self, valor):
        self.y1 = valor

    def setX2(self, valor):
        self.x2 = valor

    def setY2(self, valor):
        self.y2 = valor

    def getIzquierda(self):
        return self.izquierda
    
    def getDerecha(self):
        return self.derecha
    
    def getDato(self):
        return self.codigo

    def getNombre(self):
        return self.nombre

    def getMaterial(self):
        return self.material

    def getCantidad(self):
        return self.cantidad

    def setDato(self, valor):
        self.dato = valor

    def setCantidad(self, valor):
        self.cantidad = valor
    
    def setIzquierda(self, valor):
        self.izquierda = valor

    def setDerecha(self, valor):
        self.derecha = valor

    def setVecesVisitado(self):
        self.vecesVisitado += 1
