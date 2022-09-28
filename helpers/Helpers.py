from abc import abstractmethod
import random
from tkinter import *
from turtle import width

class Helpers:

    def __init__(self):
        pass

    @abstractmethod
    def generarCodigoAlmacenajeMaterial() -> int:
        return random.randint(0,1000)

    @abstractmethod
    def generarRecorrido(nave, arbolSistema) -> list:
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
        naves[0].setViaje(False)
        
        naves[1].setCapacidadOro(0)
        naves[1].setCapacidadPlata(0)
        naves[1].setCapacidadBronce(0)
        naves[1].setCargaLlena(False)
        naves[1].setViaje(False)

        naves[2].setCapacidadOro(0)
        naves[2].setCapacidadPlata(0)
        naves[2].setCapacidadBronce(0)
        naves[2].setCargaLlena(False)
        naves[2].setViaje(False)

        canvas.itemconfig('naveActual', text="Nave: ")
        canvas.itemconfig('oro', text="Oro: 0")
        canvas.itemconfig('plata', text="Plata: 0")
        canvas.itemconfig('bronce', text="Bronce: 0")
        canvas.moveto('nave', 40, 20)

    @abstractmethod
    def generarMateriales(canvas, arbolSistema):
        arbolSistema.resetLista()
        nodos = arbolSistema.mostrarInOrden(arbolSistema.getRaiz())
        for i in nodos:
            i.aumentarCantidad(canvas)

    @abstractmethod
    def mostrarArbol(canvas, arbolSistema, naves):
        canvas.delete("naveActual")
        canvas.delete("oro")
        canvas.delete("plata")
        canvas.delete("bronce")
        canvas.delete("unidadesAlmacen")
        canvas.delete("nodosArbolMateriales")

        canvas.create_text(40, 60, text="Nave: ", tags=["naveActual"], font=('Helvetica', 9, 'bold'), fill="white")
        canvas.create_text(40, 80, text="Oro: 0", tags=["oro"], font=('Helvetica', 9, 'bold'), fill="white")
        canvas.create_text(40, 100, text="Plata: 0", tags=["plata"], font=('Helvetica', 9, 'bold'), fill="white")
        canvas.create_text(40, 120, text="Bronce: 0", tags=["bronce"], font=('Helvetica', 9, 'bold'), fill="white")
        canvas.create_text(450, 140, text="Unid. Almacén: 0", tags=["unidadesAlmacen"], font=('Helvetica', 9, 'bold'), fill="white")
        canvas.create_text(450, 160, text="Arb Mat. Nodos: 0", tags=["nodosArbolMateriales"], font=('Helvetica', 9, 'bold'), fill="white")

        for i in arbolSistema.mostrarInOrden(arbolSistema.getRaiz()):
            color = ""
            if(i.getMaterial() == "oro"): color = "#BBA750"
            if(i.getMaterial() == "plata"): color = "#839D9E"
            if(i.getMaterial() == "bronce"): color = "#7B5F32"
            canvas.create_oval(i.getX(), i.getY(), i.getX2(), i.getY2(), fill=color)
            nombre = "{0} - {1}".format(i.getNombre(),i.getDato())
            canvas.create_text(i.getX()+10, i.getY2()+15, text=nombre,font=('Helvetica', 9, 'bold'), fill="white")
            canvas.create_text(i.getX()+10, i.getY2()+30, text=i.getCantidad(), font=('Helvetica', 9, 'bold'), tags=nombre, fill="white")

        for i in arbolSistema.mostrarInOrden(arbolSistema.getRaiz()):
            if(i.getIzquierda()):
                canvas.create_line(i.getX()+15, i.getY()+15, i.getIzquierda().getX()+15, i.getIzquierda().getY()+15,fill="red", width=2)
            if(i.getDerecha()):
                canvas.create_line(i.getX()+15, i.getY()+15, i.getDerecha().getX()+15, i.getDerecha().getY()+15, fill="blue", width=2)

    def mostrarArbolMateriales(arbolMateriales):
        materiales =  arbolMateriales.mostrarInOrden(arbolMateriales.getRaiz())
        ventanados = Tk()
        ventanados.geometry("600x600")
        ventanados.title("Arbol de materiales")
        canvasdos = Canvas(ventanados, width=550, height=600, bg='black')
        canvasdos.pack(expand=YES)

        for i in materiales:
            canvasdos.create_oval(i.getX(), i.getY(), i.getX2(), i.getY2(), fill=i.getColor())
            canvasdos.create_text(i.getTextX(), i.getY2()+15, text=i.getDato(), fill=i.getTextColor())

        for i in materiales:
            if(i.getIzquierda()):
                canvasdos.create_line(i.getX()+15, i.getY()+15, i.getIzquierda().getX()+15, i.getIzquierda().getY()+15, fill="red", width=2)
            if(i.getDerecha()):
                canvasdos.create_line(i.getX()+15, i.getY()+15, i.getDerecha().getX()+15, i.getDerecha().getY()+15, fill="blue", width=2)

        mainloop()
