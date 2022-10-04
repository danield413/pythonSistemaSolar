from datetime import datetime
import random
from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
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
    Helpers.mostrarArbolMateriales(arbolMateriales)

def generarSistema():
    for i in planetas:
        nodoPlaneta = Nodo(
            i["codigo"],
            i["nombre"],
            i["material"],
            i["cantidad"],
            i["posicionX1"],
            i["posicionY1"],
            i["posicionX2"],
            i["posicionY2"],
        )
        arbolSistema.agregar(nodoPlaneta)

    # zork = Helpers.getNodo(120, arbolSistema)
    # print(zork)
    # print(arbolSistema.cantidadNodos(arbolSistema.getRaiz()))
    # arbolSistema.eliminarNodoConHijo(arbolSistema.getRaiz(), zork)
    # print(arbolSistema.cantidadNodos(arbolSistema.getRaiz()))
    # zork = Helpers.getNodo(120, arbolSistema)
    # print("zork >>", zork)

    arbolSistema.resetLista()
    Helpers.mostrarArbol(canvas, arbolSistema)
    Helpers.generarMateriales(canvas, arbolSistema)
    naves[0].cambiarRecorrido(arbolSistema)
    naves[1].cambiarRecorrido(arbolSistema)
    naves[2].cambiarRecorrido(arbolSistema)


def pararRecoleccion():
    for i in naves:
        i.setViaje(True)
        i.setCargaLlena(True)

def reanudarRecolecion():
    for i in naves:
        i.setViaje(False)
        i.setCargaLlena(False)

def enviarNaves():
    proceso1 = empezarARecolectar("nave")
    hilo1 = threading.Thread(name="HiloNave1", target=proceso1)
    hilo1.start()

def guardarMaterialEnAlmacen(recoleccion):
    almacen.setOroAlmacenado(almacen.getOroAlmacenado() + recoleccion["oro"])
    almacen.setPlataAlmacenada(almacen.getPlataAlmacenada() + recoleccion["plata"])
    almacen.setBronceAlmacenado(almacen.getBronceAlmacenado() + recoleccion["bronce"])

    texto = "Unid. Almacén: " + str(
        almacen.getOroAlmacenado()
        + almacen.getPlataAlmacenada()
        + almacen.getBronceAlmacenado()
    )
    canvas.itemconfig("unidadesAlmacen", text=texto)

    if almacen.getOroAlmacenado() > 30:
        almacenarMaterial("oro", almacen.getOroAlmacenado())
        almacen.setOroAlmacenado(0)
    if almacen.getPlataAlmacenada() > 30:
        almacenarMaterial("plata", almacen.getPlataAlmacenada())
        almacen.setPlataAlmacenada(0)
    if almacen.getBronceAlmacenado() > 30:
        almacenarMaterial("bronce", almacen.getBronceAlmacenado())
        almacen.setBronceAlmacenado(0)

    textoNodos = "Arb Mat. Nodos: " + str(
        arbolMateriales.cantidadNodos(arbolMateriales.getRaiz())
    )
    canvas.itemconfig("nodosArbolMateriales", text=textoNodos)

def almacenarMaterial(tipoMaterial, cantidad):
    codigoAlmacenaje = Helpers.generarCodigoAlmacenajeMaterial()
    nuevoNodo = MaterialNodo(codigoAlmacenaje, datetime.now(), tipoMaterial, cantidad)
    arbolMateriales.agregar(nuevoNodo)


def finalizarRecorrido(naveActual, tarea):
    Helpers.reiniciarRecorridoNave(naves, canvas)
    naveActual.cambiarRecorrido(arbolSistema)
    canvas.after_cancel(tarea)


# ? ciclo de salidas
def empezarARecolectar(puntero):
    
    indexNave = random.randint(0, 2)
    if naves[indexNave].getEnViaje() == False:
        despacharNave(0, puntero, naves[indexNave])
        texto = "Nave: " + str(indexNave + 1)
        canvas.itemconfig("naveActual", text=texto)
        print(">> Despacho: ", texto)
        canvas.after(4000, empezarARecolectar, puntero)


# ? salida de la nave
def despacharNave(cont, puntero, naveActual):
    if naveActual.getEnViaje() is False:
        naveActual.setViaje(True)

        recolectar(
            cont,
            naveActual.getRecorrido(),
            len(naveActual.getRecorrido()) - 1,
            puntero,
            naveActual,
        )
        return

def recolectar(cont, lista, length, puntero, naveActual):
    tarea = canvas.after(250, recolectar, cont + 1, lista, length, puntero, naveActual)
    canvas.moveto(puntero, lista[cont].getX() - 4, lista[cont].getY() - 4)
    planetaActual = lista[cont]

    cantidadPlaneta = planetaActual.getCantidad()
    capacidadOro = naveActual.getCapacidadOro()
    capacidadPlata = naveActual.getCapacidadPlata()
    capacidadBronce = naveActual.getCapacidadBronce()
    restantesOro = 30 - capacidadOro
    restantesPlata = 30 - capacidadPlata
    restantesBronce = 30 - capacidadBronce

    arbolSistema.aumentarVisitas(planetaActual.getNombre(), arbolSistema.getRaiz())

    # ? puedo sacar oro
    if restantesOro < 31 and planetaActual.getMaterial() == "oro":
        # print("EXTRAIGO ORO")

        if cantidadPlaneta <= restantesOro:
            planetaActual.disminuirCantidad(cantidadPlaneta, canvas)
            naveActual.setCapacidadOro(naveActual.getCapacidadOro() + cantidadPlaneta)
            texto = "Oro: " + str(naveActual.getCapacidadOro())
            canvas.itemconfig("oro", text=texto)

        if cantidadPlaneta > restantesOro:
            planetaActual.disminuirCantidad(
                cantidadPlaneta - (cantidadPlaneta - restantesOro), canvas
            )
            naveActual.setCapacidadOro(naveActual.getCapacidadOro() + restantesOro)
            texto = "Oro: " + str(naveActual.getCapacidadOro())
            canvas.itemconfig("oro", text=texto)

    # ? puedo sacar plata
    if restantesPlata < 31 and planetaActual.getMaterial() == "plata":
        # print("EXTRAIGO PLATA")

        if cantidadPlaneta <= restantesPlata:
            planetaActual.disminuirCantidad(cantidadPlaneta, canvas)
            naveActual.setCapacidadPlata(
                naveActual.getCapacidadPlata() + cantidadPlaneta
            )
            texto = "Plata: " + str(naveActual.getCapacidadPlata())
            canvas.itemconfig("plata", text=texto)

        if cantidadPlaneta > restantesPlata:
            planetaActual.disminuirCantidad(
                cantidadPlaneta - (cantidadPlaneta - restantesPlata), canvas
            )
            naveActual.setCapacidadPlata(
                naveActual.getCapacidadPlata() + restantesPlata
            )
            texto = "Plata: " + str(naveActual.getCapacidadPlata())
            canvas.itemconfig("plata", text=texto)

    # ? puedo sacar bronce
    if restantesBronce < 31 and planetaActual.getMaterial() == "bronce":
        # print("EXTRAIGO BRONCE")

        if cantidadPlaneta <= restantesBronce:
            planetaActual.disminuirCantidad(cantidadPlaneta, canvas)
            naveActual.setCapacidadBronce(
                naveActual.getCapacidadBronce() + cantidadPlaneta
            )
            texto = "Bronce: " + str(naveActual.getCapacidadBronce())
            canvas.itemconfig("bronce", text=texto)

        if cantidadPlaneta > restantesBronce:
            planetaActual.disminuirCantidad(
                cantidadPlaneta - (cantidadPlaneta - restantesBronce), canvas
            )
            naveActual.setCapacidadBronce(
                naveActual.getCapacidadBronce() + restantesBronce
            )
            texto = "Bronce: " + str(naveActual.getCapacidadBronce())
            canvas.itemconfig("bronce", text=texto)

    recoleccion = {
        "oro": naveActual.getCapacidadOro(),
        "plata": naveActual.getCapacidadPlata(),
        "bronce": naveActual.getCapacidadBronce(),
        "fecha": datetime.now(),
    }

    if restantesOro == 0:
        # print(">>>>> ORO LLENO, DEVUELVE NAVE")
        guardarMaterialEnAlmacen(recoleccion)
        finalizarRecorrido(naveActual, tarea)

    if restantesPlata == 0:
        # print(">>>>> PLATA LLENO, DEVUELVE NAVE")
        guardarMaterialEnAlmacen(recoleccion)
        finalizarRecorrido(naveActual, tarea)

    if restantesBronce == 0:
        # print(">>>>> BRONCE LLENO, DEVUELVE NAVE")
        guardarMaterialEnAlmacen(recoleccion)
        finalizarRecorrido(naveActual, tarea)

    if cont == length:
        # print("no logró llenar la capacidad")
        guardarMaterialEnAlmacen(recoleccion)
        canvas.moveto(puntero, 40, 20)
        canvas.after_cancel(tarea)
        Helpers.reiniciarRecorridoNave(naves, canvas)


def eliminarPlaneta(nombrePlaneta):
    planeta = Helpers.getNodoPorNombre(nombrePlaneta, arbolSistema)
    print(arbolSistema.cantidadNodos(arbolSistema.getRaiz()))
    arbolSistema.eliminarNodo(planeta)
    print(arbolSistema.cantidadNodos(arbolSistema.getRaiz()))

    arbolSistema.resetLista()
    Helpers.mostrarArbol(canvas, arbolSistema)


def mostrarPlanetasVisitados():
    arbolSistema.resetListaVisitados()
    root = Tk()
    root.title("Eliminar planeta")
    root.geometry("400x200")

    labels = []
    for i in arbolSistema.retornarPlanetas(arbolSistema.getRaiz()):
        if i.getNombre() not in labels:
            labels.append(i.getNombre())


    l1 = Label(root, text="Seleccione el planeta que desea eliminar: ")
    l1.pack()

    lista_desplegable = ttk.Combobox(root, width=20)
    lista_desplegable["values"] = labels
    lista_desplegable.pack()

    Button(root, text="eliminar", command=lambda: eliminarPlaneta(lista_desplegable.get())).pack()

    root.mainloop()   

# Ventana
ventana = Tk()
ventana.geometry("600x600")
ventana.title("Proyecto Datos")
ventana.configure(background="black")

barraMenu = Menu(ventana)
mnuCrear = Button(barraMenu)
mnuRecoletar = Button(barraMenu)
mnuDestruir = Button(barraMenu)
mnuArbolMateriales = Button(barraMenu)

barraMenu.add_cascade(label="Generar Sistema", menu=mnuCrear, command=generarSistema)
barraMenu.add_cascade(label="Recolectar", menu=mnuRecoletar, command=enviarNaves)
barraMenu.add_cascade(
    label="Destruir", menu=mnuDestruir, command=mostrarPlanetasVisitados
)
barraMenu.add_cascade(
    label="Ver Arbol de Materiales", menu=mnuArbolMateriales, command=verArbolMateriales
)

ventana.config(menu=barraMenu)
Button(pady=20, bg="black", text="Flat border", relief="flat").pack()

# Gráfico
canvas = Canvas(ventana, width=550, height=400, bg="black")
canvas.pack(expand=NO)

# imagen de fondo
img = ImageTk.PhotoImage(
    Image.open("./images/galaxia.png").resize((600, 600))
)
canvas.background = img  # Keep a reference in case this code is put in a function.
canvas.create_image(0, 0, anchor=tk.NW, image=img)

# Nave
naveImg = PhotoImage(file="./images/nave.png")
canvas.create_image(40, 20, image=naveImg, tags=["nave"])

mainloop()
