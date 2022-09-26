from abc import abstractmethod
import random

from modelos.JSON import JSON
from modelos.Nodo import Nodo

class Helpers:

    def __init__(self):
        pass

    @abstractmethod
    def generarRecorrido(nave, arbolSistema):
        numeroRandom = random.randint(1,3)
        # print(">> Nave:", nave.getNumero(), "- Recorrido asignado => ", numeroRandom)
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

    @abstractmethod
    def reiniciarRecorridoNave(naves, canvas):
        naves[0].setCapacidadOro(0)
        naves[0].setCapacidadPlata(0)
        naves[0].setCapacidadBronce(0)
        naves[0].setCargaLlena(False)
        naves[1].setCapacidadOro(0)
        naves[1].setCapacidadPlata(0)
        naves[1].setCapacidadBronce(0)
        naves[1].setCargaLlena(False)
        naves[2].setCapacidadOro(0)
        naves[2].setCapacidadPlata(0)
        naves[2].setCapacidadBronce(0)
        naves[2].setCargaLlena(False)

        canvas.itemconfig('naveActual', text="Nave: ")
        canvas.itemconfig('oro', text="Oro: 0")
        canvas.itemconfig('plata', text="Plata: 0")
        canvas.itemconfig('bronce', text="Bronce: 0")
        canvas.moveto('nave', 40, 20)

    @abstractmethod
    def generarMateriales(canvas, arbolSistema):
        nodos = arbolSistema.mostrarInOrden(arbolSistema.getRaiz())
        for i in nodos:
            i.aumentarCantidad(canvas)

    @abstractmethod
    def generarSistema(canvas, arbolSistema, naves):
        aristas = JSON.leerJSON("./data/aristas.json")
        planetas = JSON.leerJSON("./data/planetas.json")
        for i in aristas:
            canvas.create_line(i["xInicio"], i["yInicio"], i["xFinal"], i["yFinal"], fill="#00969D")

        for i in planetas:
            # Planeta UI
            color = ""
            if(i["material"] == "oro"): color = "#BBA750"
            if(i["material"] == "plata"): color = "#839D9E"
            if(i["material"] == "bronce"): color = "#7B5F32"
            canvas.create_oval(i["posicionX1"], i["posicionY1"], i["posicionX2"], i["posicionY2"], fill=color)
            nombre = "{0} - {1}".format(i["nombre"],i["codigo"])
            canvas.create_text(i["textX"], i["textY"], text=nombre,font=('Helvetica', 9, 'bold'), fill="white")
            canvas.create_text(i["textX"], i["textY"]+15, text=i["cantidad"], font=('Helvetica', 9, 'bold'), tags=nombre, fill="white")
        
            codigo = i["codigo"]
            nombre = i["nombre"]
            material = i["material"]
            cantidad = i["cantidad"]
            x = i["posicionX1"]
            y = i["posicionY1"]
            x2 = i["posicionX2"]
            y2 = i["posicionY2"]
            # Se agrega al árbol
            arbolSistema.agregar(Nodo(codigo, nombre, material, cantidad, x, y, x2, y2))

        Helpers.generarMateriales(canvas, arbolSistema)
        naves[0].cambiarRecorrido(arbolSistema)
        naves[1].cambiarRecorrido(arbolSistema)
        naves[2].cambiarRecorrido(arbolSistema)