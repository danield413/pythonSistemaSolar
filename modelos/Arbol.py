class Arbol:
    def __init__(self):
        self.raiz = None
        self.lista = []
        self.listaVisitados = []

    def getRaiz(self):
        return self.raiz

    def resetLista(self):
        self.lista = []

    def resetListaVisitados(self):
        self.listaVisitados = []

    def mostrarInOrden(self, temp):
        if temp == None:
            return

        self.mostrarInOrden(temp.getIzquierda())
        self.lista.append(temp)
        self.mostrarInOrden(temp.getDerecha())
        return self.lista

    def retornarPlanetas(self, temp):
        if temp == None:
            return
        self.retornarPlanetas(temp.getIzquierda())
        if temp.getVecesVisitado() > 0 and not temp.getNombre() in self.listaVisitados:
            self.listaVisitados.append(temp)
        self.retornarPlanetas(temp.getDerecha())
        if temp.getVecesVisitado() > 0 and not temp.getNombre() in self.listaVisitados:
            self.listaVisitados.append(temp)
        return self.listaVisitados

    def aumentarVisitas(self, nombre, temp):
        if temp == None:
            return
        self.aumentarVisitas(nombre, temp.getIzquierda())
        if temp.getNombre() == nombre:
            temp.setVecesVisitado()
        self.aumentarVisitas(nombre, temp.getDerecha())
        if temp.getNombre() == nombre:
            temp.setVecesVisitado()

    def mostrarPreOrden(self, temp):
        if temp == None:
            return

        self.lista.append(temp)
        self.mostrarPreOrden(temp.getIzquierda())
        self.mostrarPreOrden(temp.getDerecha())
        return self.lista

    def mostrarPostOrden(self, temp):
        if temp == None:
            return

        self.mostrarPostOrden(temp.getIzquierda())
        self.mostrarPostOrden(temp.getDerecha())
        self.lista.append(temp)
        return self.lista

    def numeroHojasArbol(self, temp):
        if temp.getIzquierda() is None and temp.getDerecha() is None:
            return 1

        res = 0
        if temp.getIzquierda():
            res += self.numeroHojasArbol(temp.getIzquierda())
        if temp.getDerecha():
            res += self.numeroHojasArbol(temp.getDerecha())

        return res

    def cantidadNodos(self, temp):
        if temp == None:
            return 0

        res = self.cantidadNodos(temp.getIzquierda())
        res2 = self.cantidadNodos(temp.getDerecha())
        return res + res2 + 1

    def agregar(self, nodo):
        if self.raiz == None:
            self.raiz = nodo
        else:
            self.agregarABB(self.raiz, nodo)

    def agregarABB(self, temp, nodo):
        if temp == None:
            return True

        if nodo.getDato() < temp.getDato():
            if self.agregarABB(temp.getIzquierda(), nodo):
                temp.setIzquierda(nodo)

        if nodo.getDato() > temp.getDato():
            if self.agregarABB(temp.getDerecha(), nodo):
                temp.setDerecha(nodo)

        return False

    def eliminarHoja(self, temp, nodo):
        if temp.getDato() == nodo.getDato():
            # print("hojaaaa")
            #! si es hoja retorna True
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
                # Si tiene nodo con hijo
                # Izquierda = 1
                # Derecha = 2
                if temp.getIzquierda() != None or temp.getDerecha() != None:
                    if temp.getIzquierda() != None:
                        return 1
                    if temp.getDerecha() != None:
                        return 2

            if nodo.getDato() < temp.getDato():
                # Tiene nodo con hijo a la izquierda
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
                Padre.setNombre(datop.getNombre())
                Padre.setCantidad(datop.getCantidad())
                Padre.setVecesVisitadoDos(datop.getVecesVisitado())
                Padre.setMaterial(datop.getMaterial())
                #!__
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

    def Amplitud(self, dato):
        ListaA = []
        ListaA.append(self.raiz)
        i = 0
        ListaDatos = []

        while i < len(ListaA):
            Nodo = ListaA[i]
            # print("Amplitud {}".format(Nodo.getDato()))
            ListaA.pop(i)
            ListaDatos.append(Nodo)
            if Nodo.getIzq() != None:
                ListaA.append(Nodo.getIzquierda())

            if Nodo.getDerecha() != None:
                ListaA.append(Nodo.getDerecha())

        self.Recorrerlista(ListaDatos, dato)

    def Recorrerlista(self, listadatos, dato):
        print(len(listadatos))
        for x in range(0, len(listadatos)):
            if listadatos[x].getDato() == dato:
                if listadatos[x].getDato() % 2 == 0:
                    print("Puede Aterrirzar")
                else:
                    if listadatos[x + 1].getDato() != None:
                        if listadatos[x + 1].getDato() % 2 == 0:
                            print(
                                "Aterrizo donde su vecino: {}".format(
                                    listadatos[x + 1].getDato()
                                )
                            )
                        else:
                            print(
                                "Murio no pudo saltar al vecino: {}".format(
                                    listadatos[x + 1].getDato()
                                )
                            )
                    else:
                        print("No hay donde saltar murio")
