import random
from tkinter import *
import threading
from helpers.Helpers import Helpers

from modelos.Almacen import Almacen
from modelos.Arbol import Arbol
from modelos.Nave import Nave

arbolSistema = Arbol()
arbolMateriales = Arbol()
almacen = Almacen()

nave = Nave(1)
nave2 = Nave(2)
nave3 = Nave(3)
naves = [nave, nave2, nave3]

def generarSistema():
    Helpers.generarSistema(canvas, arbolSistema, naves)

def enviarNaves():
    proceso1 = empezarARecolectar('nave')
    hilo1 = threading.Thread(name="HiloNave1",target=proceso1)
    hilo1.start()

def guardarMaterialEnAlmacen(recoleccion):
    print(recoleccion)
    almacen.setOroAlmacenado(almacen.getOroAlmacenado() + recoleccion["oro"])
    almacen.setPlataAlmacenada(almacen.getPlataAlmacenada() + recoleccion["plata"])
    almacen.setBronceAlmacenado(almacen.getBronceAlmacenado() + recoleccion["bronce"])
    print("ALMACEN ORO:", almacen.getOroAlmacenado())
    print("ALMACEN PLATA:", almacen.getPlataAlmacenada())
    print("ALMACEN BRONCE:", almacen.getBronceAlmacenado())
    texto = "Unid. Almacén: " + str(almacen.getOroAlmacenado()+almacen.getPlataAlmacenada()+almacen.getBronceAlmacenado())
    canvas.itemconfig('unidadesAlmacen', text=texto)
    
def finalizarRecorrido(naveActual, tarea):
    Helpers.reiniciarRecorridoNave(naves, canvas)
    naveActual.cambiarRecorrido(arbolSistema)
    canvas.after_cancel(tarea)

#? ciclo de salidas
def empezarARecolectar(puntero): 
    indexNave = random.randint(0,2)
    if(naves[indexNave].getEnViaje() == False):
        despacharNave(0, puntero, naves[indexNave])
        texto = "Nave: " + str(indexNave+1)
        canvas.itemconfig("naveActual", text=texto)
        print(">> Despacho: ", texto)
        canvas.after(4000, empezarARecolectar, puntero)

#? salida de la nave
def despacharNave(cont, puntero, naveActual):
    if(naveActual.getEnViaje() is False):
        naveActual.setViaje(True)
        
        recolectar(cont, naveActual.getRecorrido(), len(naveActual.getRecorrido())-1, puntero, naveActual)
        return

def recolectar(cont, lista, length, puntero, naveActual):
    tarea = canvas.after(300, recolectar, cont+1, lista, length, puntero, naveActual)
    canvas.moveto(puntero, lista[cont].getX()-4, lista[cont].getY()-4)
    planetaActual = lista[cont]

    cantidadPlaneta = planetaActual.getCantidad()
    capacidadOro = naveActual.getCapacidadOro()
    capacidadPlata = naveActual.getCapacidadPlata()
    capacidadBronce = naveActual.getCapacidadBronce()
    restantesOro = 30 - capacidadOro
    restantesPlata = 30 - capacidadPlata
    restantesBronce = 30 - capacidadBronce

    # print(planetaActual.getNombre(), planetaActual.getCantidad())

    #? puedo sacar oro
    if(restantesOro < 31 and planetaActual.getMaterial() == 'oro'):
        print("EXTRAIGO ORO")

        if(cantidadPlaneta < restantesOro):
            planetaActual.disminuirCantidad(cantidadPlaneta, canvas)
            naveActual.setCapacidadOro(naveActual.getCapacidadOro() + cantidadPlaneta)
            texto = "Oro: " + str(naveActual.getCapacidadOro())
            canvas.itemconfig('oro', text=texto)

        if(cantidadPlaneta > restantesOro):
            planetaActual.disminuirCantidad(cantidadPlaneta - (cantidadPlaneta - restantesOro), canvas)
            naveActual.setCapacidadOro(naveActual.getCapacidadOro() + restantesOro )
            texto = "Oro: " + str(naveActual.getCapacidadOro())
            canvas.itemconfig('oro', text=texto)

    #? puedo sacar plata
    if(restantesPlata < 31 and planetaActual.getMaterial() == 'plata'):
        print("EXTRAIGO PLATA")

        if(cantidadPlaneta < restantesPlata):
            planetaActual.disminuirCantidad(cantidadPlaneta, canvas)
            naveActual.setCapacidadPlata(naveActual.getCapacidadPlata() + cantidadPlaneta)
            texto = "Plata: " + str(naveActual.getCapacidadPlata())
            canvas.itemconfig('plata', text=texto)

        if(cantidadPlaneta > restantesPlata):
            planetaActual.disminuirCantidad(cantidadPlaneta - (cantidadPlaneta - restantesPlata), canvas)
            naveActual.setCapacidadPlata(naveActual.getCapacidadPlata() + restantesPlata)
            texto = "Plata: " + str(naveActual.getCapacidadPlata())
            canvas.itemconfig('plata', text=texto)

    #? puedo sacar bronce
    if(restantesBronce < 31 and planetaActual.getMaterial() == 'bronce'):
        print("EXTRAIGO BRONCE")

        if(cantidadPlaneta < restantesBronce):
            planetaActual.disminuirCantidad(cantidadPlaneta, canvas)
            naveActual.setCapacidadBronce(naveActual.getCapacidadBronce() + cantidadPlaneta)
            texto = "Bronce: " + str(naveActual.getCapacidadBronce())
            canvas.itemconfig('bronce', text=texto)

        if(cantidadPlaneta > restantesBronce):
            planetaActual.disminuirCantidad(cantidadPlaneta - (cantidadPlaneta - restantesBronce), canvas)
            naveActual.setCapacidadBronce(naveActual.getCapacidadBronce() + restantesBronce )
            texto = "Bronce: " + str(naveActual.getCapacidadBronce())
            canvas.itemconfig('bronce', text=texto)

    recoleccion = {
        "oro": naveActual.getCapacidadOro(),
        "plata": naveActual.getCapacidadPlata(),
        "bronce": naveActual.getCapacidadBronce()
    }

    if(restantesOro == 0): 
        print(">>>>> ORO LLENO, DEVUELVE NAVE")
        guardarMaterialEnAlmacen(recoleccion)
        finalizarRecorrido(naveActual, tarea)

    if(restantesPlata == 0): 
        print(">>>>> PLATA LLENO, DEVUELVE NAVE")
        guardarMaterialEnAlmacen(recoleccion)
        finalizarRecorrido(naveActual, tarea)
        
    if(restantesBronce == 0): 
        print(">>>>> BRONCE LLENO, DEVUELVE NAVE")
        guardarMaterialEnAlmacen(recoleccion)
        finalizarRecorrido(naveActual, tarea)

    if(cont == length):
        print("no logró llenar la capacidad")
        guardarMaterialEnAlmacen(recoleccion)
        canvas.moveto(puntero, 40, 20)
        canvas.after_cancel(tarea)
        Helpers.reiniciarRecorridoNave(naves, canvas)

#Ventana
ventana = Tk()
ventana.geometry("600x600")
ventana.title("Proyecto Datos")
ventana.configure(background="black")
Button(ventana, text="Generar sistema", foreground="white", background="black",  padx=5, pady=5, command=generarSistema, font=('Helvetica', 9, 'bold')).pack()
Button(ventana, text="Recolectar", foreground="white", background="black", padx=5, pady=5, font=('Helvetica', 9, 'bold'), command=enviarNaves).pack()
Button(ventana, text="Destruir", foreground="white", background="black", padx=5, pady=5, font=('Helvetica', 9, 'bold')).pack()
Button(ventana, text="Ver arbol de materiales", foreground="white", background="black", padx=5, pady=5, font=('Helvetica', 9, 'bold')).pack()

#Gráfico
canvas = Canvas(ventana, width=550, height=400, bg='black')
canvas.pack(expand=YES)
naveImg = PhotoImage(file='./images/nave.png')
canvas.create_image(40,20, image=naveImg, tags=["nave"])

canvas.create_text(40, 60, text="Nave: ", tags=["naveActual"], font=('Helvetica', 9, 'bold'), fill="white")
canvas.create_text(40, 80, text="Oro: 0", tags=["oro"], font=('Helvetica', 9, 'bold'), fill="white")
canvas.create_text(40, 100, text="Plata: 0", tags=["plata"], font=('Helvetica', 9, 'bold'), fill="white")
canvas.create_text(40, 120, text="Bronce: 0", tags=["bronce"], font=('Helvetica', 9, 'bold'), fill="white")
canvas.create_text(450, 140, text="Unid. Almacén: 0", tags=["unidadesAlmacen"], font=('Helvetica', 9, 'bold'), fill="white")
canvas.create_text(450, 160, text="Arb Mat. Nodos: 0", tags=["nodosArbolMateriales"], font=('Helvetica', 9, 'bold'), fill="white")

mainloop()