import random

class Arbol:

    def __init__ (self):
        self.raiz = None
        self.lista = []

    def getRaiz(self):
        return self.raiz 

    def resetLista(self):
        self.lista = []   

    # #? Determina que tipo de recorrido hará la nave (puntero)
    # def hacerRecorrido(self, canvas, puntero):
    #     print("ejecucion",puntero)
    #     tipoRecorrido = random.randint(1,3)
    #     self.resetLista()
    #     if(tipoRecorrido == 1): self.mostrarInOrden(self.getRaiz())
    #     if(tipoRecorrido == 2): self.mostrarPreOrden(self.getRaiz())
    #     if(tipoRecorrido == 3): self.mostrarPostOrden(self.getRaiz())

    #     self.recolectar(canvas, 0, puntero)

    # #? nos permite recolectar los materiales mientra hacemos el recorrido seleccionado
    # def recolectar(self, canvas, cont, puntero):
    #     # print(cont, length)
    #     if(cont <= len(self.lista)-1): 
    #         canvas.moveto(puntero, self.lista[cont].getX()-4, self.lista[cont].getY()-4)

    #     tarea = canvas.after(1000, self.recolectar, canvas, cont+1, puntero)
    #     if(cont == len(self.lista)-1): 
    #         canvas.after_cancel(tarea)
    #         return

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

    def numeroHojasArbol(self, temp):
        if(temp.getIzquierda() is None and temp.getDerecha() is None):
            return 1
        
        res = 0
        if(temp.getIzquierda()): 
            res += self.numeroHojasArbol(temp.getIzquierda())
        if(temp.getDerecha()):  
            res += self.numeroHojasArbol(temp.getDerecha())
        
        return res

    def cantidadNodos(self, temp):
        if(temp == None):
            return 0
        
        res =  self.cantidadNodos(temp.getIzquierda()) 
        res2 = self.cantidadNodos(temp.getDerecha())        
        return res + res2 + 1

    def agregar(self, nodo):
        if(self.raiz == None):
            self.raiz = nodo
        else:
            self.agregarABB(self.raiz, nodo)
    
    def agregarABB(self, temp, nodo):
        if(temp == None):
            return True

        if(nodo.getDato() < temp.getDato()):
            if(self.agregarABB(temp.getIzquierda(), nodo)):
                temp.setIzquierda(nodo)

        if(nodo.getDato() > temp.getDato()):
            if(self.agregarABB(temp.getDerecha(), nodo)):
                temp.setDerecha(nodo)

        return False

    def eliminarHoja(self, temp, nodo):
        if(temp.getDato() == nodo.getDato()):
            #! si es hoja retorna True
            if(temp.getIzquierda() == None and temp.getDerecha() == None):
                return True
            
        if(nodo.getDato() < temp.getDato()):
            if( self.eliminarHoja(temp.getIzquierda(), nodo) ):
                temp.setIzquierda(None)
                
        if(nodo.getDato() > temp.getDato()):
            if( self.eliminarHoja(temp.getDerecha(), nodo) ):
                temp.setDerecha(None)
                
        return False

    def eliminarNodoConHijo(self, temp, nodo):
        if(temp.getDato() == nodo.getDato()):
            # Si tiene nodo con hijo
            # Izquierda = 1
            # Derecha = 2
            if(temp.getIzquierda() != None or temp.getDerecha() != None):
                if(temp.getIzquierda() != None):
                    return 1
                if(temp.getDerecha() != None):
                    return 2
        
        if(nodo.getDato() < temp.getDato()):
            #Tiene nodo con hijo a la izquierda
            if( self.eliminarNodoConHijo(temp.getIzquierda(), nodo) == 1 ):
                temp.setIzquierda( temp.getIzquierda().getIzquierda() )
            if( self.eliminarNodoConHijo(temp.getIzquierda(), nodo) == 2 ):
                temp.setIzquierda( temp.getIzquierda().getDerecha() )
            
        if(nodo.getDato() > temp.getDato()):
             #Tiene nodo con hijo a la derecha
            if( self.eliminarNodoConHijo(temp.getDerecha(), nodo) == 1 ):
                temp.setDerecha( temp.getDerecha().getDerecha() )
            if( self.eliminarNodoConHijo(temp.getDerecha(), nodo) == 2 ):
                temp.setDerecha( temp.getDerecha().getIzquierda() )
                
        return False

    def eliminarNodoConDosHijos(self,Padre,nodo):
        if Padre==None:
            return False

        if Padre.getDato() == nodo.getDato():
            if Padre.getIzq() != None and Padre.getDer() != None:
                datop=self.Predecesor(Padre.getIzq())
                if self.eliminarHoja(Padre.getIzq(),datop):
                    Padre.setIzq(None)

                self.eliminarNodoConHijo(Padre.getIzq(),datop)
                Padre.setDato(datop)
                return True

        if nodo.getDato() < Padre.getDato():
            if self.eliminarNodoConDosHijos(Padre.getIzq(),nodo):
                return False
        if nodo.getDato() > Padre.getDato():
            if self.eliminarNodoConDosHijos(Padre.getDer(),nodo) :
                return False

        return  False

    def Predecesor(self,Padre):
        if Padre.getDer()!=None:
            return(self.Predecesor(Padre.getDer()))
        else:
            return Padre.getDato()

    def eliminarNodo(self, nodo):
        self.eliminarHoja(self.raiz, nodo)
        self.eliminarNodoConHijo(self.raiz, nodo)
        self.eliminarNodoConDosHijos(self.raiz, nodo)

    def Amplitud(self,dato):
        ListaA=[]
        ListaA.append(self.Raiz)
        i=0;
        ListaDatos=[];

        while i<len(ListaA):
            Nodo=ListaA[i]
           # print("Amplitud {}".format(Nodo.getDato()))
            ListaA.pop(i)
            ListaDatos.append(Nodo);
            if Nodo.getIzq()!=None:
                ListaA.append(Nodo.getIzq())

            if Nodo.getDer() != None:
                ListaA.append(Nodo.getDer())

        self.Recorrerlista(ListaDatos,dato)

    def Recorrerlista(self,listadatos,dato):
        print(len(listadatos))
        for x in range(0, len(listadatos)):
            if listadatos[x].getDato()==dato:
                if listadatos[x].getDato()%2==0:
                    print("Puede Aterrirzar")
                else:
                    if listadatos[x+1].getDato()!=None:
                        if listadatos[x+1].getDato()%2==0:
                            print("Aterrizo donde su vecino: {}".format(listadatos[x+1].getDato()))
                        else:
                            print("Murio no pudo saltar al vecino: {}".format(listadatos[x+1].getDato()))
                    else:
                        print("No hay donde saltar murio")