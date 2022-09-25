class Nodo:

    def __init__(self, codigo, nombre, material, cantidad, x, y, x2, y2):
        self.vecesVisitado = 0
        self.izquierda = None
        self.derecha = None
        self.codigo = codigo
        self.nombre = nombre
        self.material = material
        self.cantidad = cantidad
        self.coordenadaX1 = x
        self.coordenadaY1 = y
        self.coordenadaX2 = x2
        self.coordenadaY2 = y2

    def setVecesVisitado(self):
        self.vecesVisitado += 1

    def aumentarCantidad(self, canvas):
        self.cantidad += 2
        canvas.itemconfig(self.nombre, text=str( self.cantidad ))
        canvas.after(10000, self.aumentarCantidad, canvas)

    def disminuirCantidad(self, valor, canvas):
        self.cantidad -= valor
        canvas.itemconfig(self.nombre, text=self.cantidad)

    def getInformacion(self):
        return "Nombre: {0} - Código: {1} - Material: {2} - Cantidad: {3}".format(self.nombre, self.codigo, self.material, self.cantidad)

    def getX(self):
        return self.coordenadaX1

    def getY(self):
        return self.coordenadaY1

    def getX2(self):
        return self.coordenadaX2

    def getY2(self):
        return self.coordenadaY2

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
