class MaterialArbol:

    def __init__ (self):
        self.raiz = None
        self.lista = []
        self.listaPrueba = []

    def getRaiz(self):
        return self.raiz 

    def resetLista(self):
        self.lista = []   

    def mostrarInOrden(self, temp):
        if(temp == None): return
        
        self.mostrarInOrden(temp.getIzquierda())
        self.lista.append(temp)
        self.mostrarInOrden(temp.getDerecha())
        return self.lista
        
    def mostrarPreOrden(self, temp):
        if(temp == None): return
        
        self.lista.append(temp)
        self.mostrarPreOrden(temp.getIzquierda())
        self.mostrarPreOrden(temp.getDerecha())
        return self.lista
        
    def mostrarPostOrden(self, temp):
        if(temp == None): return
        
        self.mostrarPostOrden(temp.getIzquierda())
        self.mostrarPostOrden(temp.getDerecha())
        self.lista.append(temp)
        return self.lista

    def cantidadNodos(self, temp):
        if(temp == None):
            return 0
        
        res =  self.cantidadNodos(temp.getIzquierda()) 
        res2 = self.cantidadNodos(temp.getDerecha())        
        return res + res2 + 1

    def agregar(self, nodo):
        if(self.raiz == None):
            self.raiz = nodo
            nodo.setX(250)
            nodo.setY(20)
            nodo.setX2(280)
            nodo.setY2(50)
            nodo.setTextX(250)
        else:
            self.agregarABB(self.raiz, nodo)
    
    def agregarABB(self, temp, nodo):
        if(temp == None):
            return True

        if(nodo.getDato() < temp.getDato()):
            if(self.agregarABB(temp.getIzquierda(), nodo)):
                temp.setIzquierda(nodo)
                temp.getIzquierda().setX(temp.getX()-40)
                temp.getIzquierda().setY(temp.getY()+60)
                temp.getIzquierda().setX2(temp.getX2()-40)
                temp.getIzquierda().setY2(temp.getY2()+60)
                temp.getIzquierda().setTextX(temp.getX()-50)
                temp.getIzquierda().setTextColor("green")
                temp.getIzquierda().setColor('green')

        if(nodo.getDato() > temp.getDato()):
            if(self.agregarABB(temp.getDerecha(), nodo)):
                temp.setDerecha(nodo)
                temp.getDerecha().setX(temp.getX()+40)
                temp.getDerecha().setY(temp.getY()+40)
                temp.getDerecha().setX2(temp.getX2()+40)
                temp.getDerecha().setY2(temp.getY2()+40)
                temp.getDerecha().setTextX(temp.getX()+50)
                temp.getDerecha().setTextColor("purple")
                temp.getDerecha().setColor('purple')

        return False

    def eliminarHoja(self, temp, nodo):
        if temp.getDato() == nodo.getDato():
            if temp.getIzquierda() == None and temp.getDerecha() == None:
                return True

        if nodo.getDato() < temp.getDato():
            if self.eliminarHoja(temp.getIzquierda(), nodo):
                temp.setIzquierda(None)

        if nodo.getDato() > temp.getDato():
            if self.eliminarHoja(temp.getDerecha(), nodo):
                temp.setDerecha(None)

        return False

    def eliminarNodoConHijo(self, temp, nodo):
        if temp != None:
            if temp.getDato() == nodo.getDato():
               
                if temp.getIzquierda() != None or temp.getDerecha() != None:
                    if temp.getIzquierda() != None:
                        return 1
                    if temp.getDerecha() != None:
                        return 2

            if nodo.getDato() < temp.getDato():
                if self.eliminarNodoConHijo(temp.getIzquierda(), nodo) == 1:
                    temp.setIzquierda(temp.getIzquierda().getIzquierda())
                if self.eliminarNodoConHijo(temp.getIzquierda(), nodo) == 2:
                    temp.setIzquierda(temp.getIzquierda().getDerecha())

            if nodo.getDato() > temp.getDato():
                # Tiene nodo con hijo a la derecha
                if self.eliminarNodoConHijo(temp.getDerecha(), nodo) == 1:
                    temp.setDerecha(temp.getDerecha().getIzquierda())
                if self.eliminarNodoConHijo(temp.getDerecha(), nodo) == 2:
                    temp.setDerecha(temp.getDerecha().getDerecha())

            return False

    def eliminarNodoConDosHijos(self, Padre, nodo):
        if Padre == None:
            return False

        if Padre.getDato() == nodo.getDato():
            if Padre.getIzquierda() != None and Padre.getDerecha() != None:
                datop = self.Predecesor(Padre.getIzquierda())
                if self.eliminarHoja(Padre.getIzquierda(), datop):
                    Padre.setIzquierda(None)

                self.eliminarNodoConHijo(Padre.getIzquierda(), datop)
                Padre.setDato(datop.getDato())
                Padre.setCantidad(datop.getCantidad())
                Padre.setMaterial(datop.getMaterial())
                Padre.setFecha(datop.getFecha())
                return True

        if nodo.getDato() < Padre.getDato():
            if self.eliminarNodoConDosHijos(Padre.getIzquierda(), nodo):
                return False
        if nodo.getDato() > Padre.getDato():
            if self.eliminarNodoConDosHijos(Padre.getDerecha(), nodo):
                return False

        return False

    def Predecesor(self, Padre):
        if Padre.getDerecha() != None:
            return self.Predecesor(Padre.getDerecha())
        else:
            return Padre

    def eliminarNodo(self, nodo):
        self.eliminarHoja(self.raiz, nodo)
        self.eliminarNodoConHijo(self.raiz, nodo)
        self.eliminarNodoConDosHijos(self.raiz, nodo)