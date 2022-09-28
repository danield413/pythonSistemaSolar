from datetime import datetime
import random
from tkinter import *
import threading
from helpers.Helpers import Helpers

from modelos.Almacen import Almacen
from modelos.Arbol import Arbol
from modelos.JSON import JSON
from modelos.MaterialArbol import MaterialArbol
from modelos.MaterialNodo import MaterialNodo
from modelos.Nave import Nave
from modelos.Nodo import Nodo

arbolSistema = Arbol()
arbolMateriales = MaterialArbol()
almacen = Almacen()

nave = Nave(1)
nave2 = Nave(2)
nave3 = Nave(3)
naves = [nave, nave2, nave3]
planetas = JSON.leerJSON("./data/planetas.json")

def verArbolMateriales():
    pararRecoleccion()
    Helpers.mostrarArbolMateriales(arbolMateriales)
    
def generarSistema():
    for i in planetas:
        nodoPlaneta = Nodo(i["codigo"], i["nombre"], i["material"], i["cantidad"], i["posicionX1"], i["posicionY1"], i["posicionX2"], i["posicionY2"])
        arbolSistema.agregar(nodoPlaneta)

    Helpers.mostrarArbol(canvas, arbolSistema, naves)
    Helpers.generarMateriales(canvas, arbolSistema)
    naves[0].cambiarRecorrido(arbolSistema)
    naves[1].cambiarRecorrido(arbolSistema)
    naves[2].cambiarRecorrido(arbolSistema)

def pararRecoleccion():
    for i in naves:
        i.setViaje(True)
        i.setCargaLlena(True)

def reanudarRecollecion():
    for i in naves:
        i.setViaje(False)
        i.setCargaLlena(False)

def buscarPlaneta(nombre) -> object:
    for i in planetas:
        if(i["nombre"] == nombre): return i
    else: None

def enviarNaves():
    proceso1 = empezarARecolectar('nave')
    hilo1 = threading.Thread(name="HiloNave1",target=proceso1)
    hilo1.start()

def guardarMaterialEnAlmacen(recoleccion):
    almacen.setOroAlmacenado(almacen.getOroAlmacenado() + recoleccion["oro"])
    almacen.setPlataAlmacenada(almacen.getPlataAlmacenada() + recoleccion["plata"])
    almacen.setBronceAlmacenado(almacen.getBronceAlmacenado() + recoleccion["bronce"])
    
    texto = "Unid. Almacén: " + str(almacen.getOroAlmacenado()+almacen.getPlataAlmacenada()+almacen.getBronceAlmacenado())
    canvas.itemconfig('unidadesAlmacen', text=texto)

    if(almacen.getOroAlmacenado() > 30):
       almacenarMaterial("oro", almacen.getOroAlmacenado())
    if(almacen.getPlataAlmacenada() > 30):
       almacenarMaterial("plata", almacen.getPlataAlmacenada())
    if(almacen.getBronceAlmacenado() > 30):
        almacenarMaterial("bronce", almacen.getBronceAlmacenado())

    textoNodos = "Arb Mat. Nodos: " +  str(arbolMateriales.cantidadNodos(arbolMateriales.getRaiz()))
    canvas.itemconfig('nodosArbolMateriales', text=textoNodos)    

def almacenarMaterial(tipoMaterial, cantidad):
    codigoAlmacenaje = Helpers.generarCodigoAlmacenajeMaterial()
    nuevoNodo = MaterialNodo(codigoAlmacenaje, datetime.now(), tipoMaterial, cantidad)
    arbolMateriales.agregar(nuevoNodo)

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
        canvas.after(3000, empezarARecolectar, puntero)

#? salida de la nave
def despacharNave(cont, puntero, naveActual):
    if(naveActual.getEnViaje() is False):
        naveActual.setViaje(True)
        
        recolectar(cont, naveActual.getRecorrido(), len(naveActual.getRecorrido())-1, puntero, naveActual)
        return

def recolectar(cont, lista, length, puntero, naveActual):
    tarea = canvas.after(250, recolectar, cont+1, lista, length, puntero, naveActual)
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
        # print("EXTRAIGO ORO")

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
        # print("EXTRAIGO PLATA")

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
        # print("EXTRAIGO BRONCE")

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
        "bronce": naveActual.getCapacidadBronce(),
        "fecha": datetime.now()
    }

    if(restantesOro == 0): 
        # print(">>>>> ORO LLENO, DEVUELVE NAVE")
        guardarMaterialEnAlmacen(recoleccion)
        finalizarRecorrido(naveActual, tarea)

    if(restantesPlata == 0): 
        # print(">>>>> PLATA LLENO, DEVUELVE NAVE")
        guardarMaterialEnAlmacen(recoleccion)
        finalizarRecorrido(naveActual, tarea)
        
    if(restantesBronce == 0): 
        # print(">>>>> BRONCE LLENO, DEVUELVE NAVE")
        guardarMaterialEnAlmacen(recoleccion)
        finalizarRecorrido(naveActual, tarea)

    if(cont == length):
        # print("no logró llenar la capacidad")
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
Button(ventana, text="Ver arbol de materiales", foreground="white", background="black", padx=5, pady=5, font=('Helvetica', 9, 'bold'), command=verArbolMateriales).pack()

#Gráfico
canvas = Canvas(ventana, width=550, height=400, bg='black')
canvas.pack(expand=NO)
naveImg = PhotoImage(file='./images/nave.png')
canvas.create_image(40,20, image=naveImg, tags=["nave"])

mainloop()