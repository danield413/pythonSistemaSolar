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



""" Crea las instancias del arbol de planetas, del arbol de materiales y del almacen 
    Crea las instancias de las naves
    Carga los planetas desde el archivo JSON 
"""
arbolSistema = Arbol()
arbolMateriales = MaterialArbol()
almacen = Almacen()

nave = Nave(1)
nave2 = Nave(2)
nave3 = Nave(3)
naves = [nave, nave2, nave3]
planetas = JSON.leerJSON("./data/planetas.json")


"""
    Muestra el arbol de materiales solo si hay almenos un Nodo
"""
def verArbolMateriales():
    if(arbolMateriales.getRaiz() != None):
        Helpers.mostrarArbolMateriales(arbolMateriales)
    else:
        print("No hay materiales almacenados")

"""
    Retorna True si hay almenos una nave en recorrido
    :return: un valor Booleano.
"""
def hayNavesEnRecorrido() -> bool:
    for i in naves:
        if(i.getEnViaje()):
            return True
    return False

"""
    Crea el arbol cargandolo del archivo <planetas.json> en la clase Arbol y en la interfaz
"""
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

    arbolSistema.resetLista()
    Helpers.mostrarArbol(canvas, arbolSistema)
    Helpers.generarMateriales(canvas, arbolSistema)
    naves[0].cambiarRecorrido(arbolSistema)
    naves[1].cambiarRecorrido(arbolSistema)
    naves[2].cambiarRecorrido(arbolSistema)



"""
    Crea un Hilo donde se ejecuta la recoleccion de materiales
    El hilo permite ejecutar la recoleccion de materiales en paralelo
"""
def enviarNaves():
    proceso1 = empezarARecolectar()
    hilo1 = threading.Thread(name="HiloNave1", target=proceso1)
    hilo1.start()


"""
    Toma un diccionario de materiales resultado de la recolección de una nave, 
    los añade al almacén, y si el almacén tiene más de 30 unidades de cualquier material, 
    los almacena en un árbol de materiales.

    :param recoleccion: un diccionario con los materiales recolectados.
"""
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



"""
    Crea un nuevo Nodo en el arbol de materiales

    :param tipoMaterial: String
    :param cantidad: int
"""
def almacenarMaterial(tipoMaterial, cantidad):
    codigoAlmacenaje = Helpers.generarCodigoAlmacenajeMaterial()
    nuevoNodo = MaterialNodo(codigoAlmacenaje, datetime.now(), tipoMaterial, cantidad)
    arbolMateriales.agregar(nuevoNodo)


"""
    Finaliza el recorrido de la nave pasada como argumento y
    cancela la siguiente tarea programada para la nave.

    :param naveActual: La instancia de la nave que se desea cancelar.
    :param tarea: la tarea programada para la nave.
"""
def finalizarRecorrido(naveActual, tarea):
    Helpers.reiniciarRecorridoNave(naves, canvas)
    naveActual.cambiarRecorrido(arbolSistema)
    canvas.after_cancel(tarea)



"""
    Se encarga de seleccionar una nave aleatoria que esté disponible para realizar un recorrido
    y llama al método "despachar nave".
    Esta función se ejecuta cada 30 segundos (30000 milisegundos).
"""
def empezarARecolectar():
    indexNave = random.randint(0, 2)
    if naves[indexNave].getEnViaje() == False:
        despacharNave(0, naves[indexNave])
        texto = "Nave: " + str(indexNave + 1)
        canvas.itemconfig("naveActual", text=texto)
        print(">> Despacho: ", texto)
        canvas.after(30000, empezarARecolectar)



"""
    Si la nave no está en viaje ejecuta la función recolectar.

    :param cont: un contador para saber en que nodo de la ruta se encuentra la nave.
    :param naveActual: la instancia de la Nave que hará el recorrido
"""
def despacharNave(cont, naveActual):
    if naveActual.getEnViaje() is False:
        naveActual.setViaje(True)

        recolectar(
            cont,
            naveActual.cambiarRecorrido(arbolSistema),
            len(naveActual.getRecorrido()) - 1,
            naveActual,
        )

"""
    Mueve la nave espacial por la pantalla y el arbol al mismo tiempo, 
    recogiendo recursos de los planetas

    :param cont: la posición actual en la ruta de la nave.
    :param lista: lista de planetas (nodos) que recorrerá la nave.
    :param length: la longitud de la lista de planetas.
    :param naveActual: la instancia de la nave que hace el recorrido.
"""
def recolectar(cont, lista, length, naveActual):
    tarea = canvas.after(1000, recolectar, cont + 1, lista, length, naveActual)
    canvas.moveto("nave", lista[cont].getX() - 4, lista[cont].getY() - 4)
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
        print(">> La nave se devolvió, esperando el despacho de otra nave...")
        guardarMaterialEnAlmacen(recoleccion)
        finalizarRecorrido(naveActual, tarea)

    if restantesPlata == 0:
        print(">> La nave se devolvió, esperando el despacho de otra nave...")
        guardarMaterialEnAlmacen(recoleccion)
        finalizarRecorrido(naveActual, tarea)

    if restantesBronce == 0:
        print(">> La nave se devolvió, esperando el despacho de otra nave...")
        guardarMaterialEnAlmacen(recoleccion)
        finalizarRecorrido(naveActual, tarea)

    if cont == length:
        print(">> La nave se devolvió, esperando el despacho de otra nave...")
        guardarMaterialEnAlmacen(recoleccion)
        canvas.moveto("nave", 40, 20)
        canvas.after_cancel(tarea)
        Helpers.reiniciarRecorridoNave(naves, canvas)


"""
    Elimina un nodo del árbol, luego reinicia el árbol y lo dibuja de nuevo

    :param nombrePlaneta: el nombre del planeta a eliminar
"""
def eliminarPlaneta(nombrePlaneta):
    planeta = Helpers.getNodoPorNombre(nombrePlaneta, arbolSistema)
    print(arbolSistema.cantidadNodos(arbolSistema.getRaiz()))
    arbolSistema.eliminarNodo(planeta)
    print(arbolSistema.cantidadNodos(arbolSistema.getRaiz()))
    
    arbolSistema.resetLista()
    Helpers.mostrarArbol(canvas, arbolSistema)
       
"""
    Crea una ventana con un menú desplegable de planetas, y al pulsar el botón, 
    llama a la función función eliminarPlaneta() con el planeta seleccionado como parámetro.
"""
def mostrarPlanetasVisitados():
    arbolSistema.resetListaVisitados()
    if not hayNavesEnRecorrido():
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
    else:
        print("no se puede, eliminar hay naves en recorrido")

""" Crea la ventana principal de la aplicación, añade el menú, los botones y el Gráfico canvas."""
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

canvas.create_text(
    450,
    140,
    text="Unid. Almacén: 0",
    tags=["unidadesAlmacen"],
    font=("Helvetica", 9, "bold"),
    fill="black",
)
canvas.create_text(
    450,
    160,
    text="Arb Mat. Nodos: 0",
    tags=["nodosArbolMateriales"],
    font=("Helvetica", 9, "bold"),
    fill="black",
)

mainloop()
