from abc import abstractmethod
import random

class Helpers:

    def __init__(self):
        pass

    @abstractmethod
    def generarRecorrido(nave, arbolSistema):
        numeroRandom = random.randint(1,3)
        print(">> Nave:", nave.getNumero(), "- Recorrido asignado => ", numeroRandom)
        recorrido = []
        arbolSistema.resetLista()
        if(numeroRandom == 1): recorrido = arbolSistema.mostrarInOrden(arbolSistema.getRaiz())
        if(numeroRandom == 2): recorrido = arbolSistema.mostrarPreOrden(arbolSistema.getRaiz())
        if(numeroRandom == 3): recorrido = arbolSistema.mostrarPostOrden(arbolSistema.getRaiz())
        return recorrido

    @abstractmethod
    def volver(puntero, canvas):
        if(puntero == "puntero"): canvas.moveto(puntero,0,0)
        if(puntero == "puntero2"): canvas.moveto(puntero,40,0)
        if(puntero == "puntero3"): canvas.moveto(puntero,80,0)