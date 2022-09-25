import random
from tkinter import *
import threading

from helpers.Helpers import Helpers
from modelos.Arbol import Arbol
from modelos.Nave import Nave
from modelos.Nodo import Nodo
from modelos.JSON import JSON

arbolSistema = Arbol()
arbolMateriales = Arbol()
nave = Nave(1, "blue")
nave2 = Nave(2, "red")
nave3 = Nave(3, "green")
naves = [nave, nave2, nave3]
#En milisegundos
VELOCIDAD_NODOS = 250
VELOCIDAD_SALIDA = 4000

def reiniciarCapacidadNaves():
    naves[0].setCapacidad(0)
    naves[1].setCapacidad(0)
    naves[2].setCapacidad(0)

def generarMateriales():
    nodos = arbolSistema.mostrarInOrden(arbolSistema.getRaiz())
    for i in nodos:
        i.aumentarCantidad(canvas)

def generarSistema():
    aristas = JSON.leerJSON("./data/aristas.json")
    planetas = JSON.leerJSON("./data/planetas.json")
    for i in aristas:
        canvas.create_line(i["xInicio"], i["yInicio"], i["xFinal"], i["yFinal"], fill="#272727")

    for i in planetas:
        # Planeta UI
        color = ""
        if(i["material"] == "oro"): color = "#BBA750"
        if(i["material"] == "plata"): color = "#839D9E"
        if(i["material"] == "bronce"): color = "#7B5F32"
        canvas.create_oval(i["posicionX1"], i["posicionY1"], i["posicionX2"], i["posicionY2"], fill=color)
        nombre = "{0} - {1}".format(i["nombre"],i["codigo"])
        canvas.create_text(i["textX"], i["textY"], text=nombre,font=('Helvetica', 9, 'bold'))
        canvas.create_text(i["textX"], i["textY"]+15, text=i["cantidad"], font=('Helvetica', 9, 'bold'), tags=nombre)
    
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

    generarMateriales()
    nave.cambiarRecorrido(arbolSistema)
    nave2.cambiarRecorrido(arbolSistema)
    nave3.cambiarRecorrido(arbolSistema)

def enviarNaves():

        proceso1 = empezarARecolectar('puntero')
        # proceso2 = empezarARecolectar('puntero2', nave2)
        # proceso3 = empezarARecolectar('puntero3', nave3)

        hilo1 = threading.Thread(name="HiloNave1",target=proceso1)
        # hilo2 = threading.Thread(name="HiloNave2",target=proceso2)
        # hilo3 = threading.Thread(name="HiloNave3",target=proceso3)

        hilo1.start()
        # hilo2.start()
        # hilo3.start()

#? ciclo de salidas
def empezarARecolectar(puntero): 
    indexNave = random.randint(0,2)
    if(naves[indexNave].getEnViaje() == False):
        canvas.itemconfig(puntero, fill=naves[indexNave].getColor())
        despacharNave(0, puntero, naves[indexNave])

        canvas.after(20000, empezarARecolectar, puntero)

#? salida de la nave
def despacharNave(cont, puntero, naveActual):
       
    if(naveActual.getEnViaje() is False):
        naveActual.setViaje(True)
        
        recolectar(cont, naveActual.getRecorrido(), len(naveActual.getRecorrido())-1, puntero, naveActual)
        # canvas.after(4000, despacharNave, 0, puntero, naveActual)
        return

#? recoleccion de materiales en los planetas
def recolectar(cont, lista, length, puntero, naveActual):
    tarea = canvas.after(2000, recolectar, cont+1, lista, length, puntero, naveActual)

    if(cont >= length):
        naveActual.setViaje(False)
        Helpers.volver(puntero, canvas)
        canvas.after_cancel(tarea)
        naveActual.cambiarRecorrido(arbolSistema)
        return

    planetaActual = lista[cont]
    cantidadPlaneta = planetaActual.getCantidad()
    capacidadNave = naveActual.getCapacidad()
    restantesNave = 30 - capacidadNave
    print(nave.getNumero(), "DISPONIBLE: ", restantesNave)
    if(restantesNave < 31):
        if(cantidadPlaneta < restantesNave):
            #22 - 30
            # print("quitó a")
            planetaActual.disminuirCantidad(cantidadPlaneta, canvas)
            naveActual.setCapacidad(naveActual.getCapacidad() + cantidadPlaneta)

        if(cantidadPlaneta > restantesNave):
            #90 - 20
            # 90 - (90-20)
            # print("quitó b")
            planetaActual.disminuirCantidad(cantidadPlaneta - (cantidadPlaneta - restantesNave), canvas)
            naveActual.setCapacidad(naveActual.getCapacidad() + restantesNave )

    if(restantesNave == 0 and cont >= length):
        print("Nave devuelta a la base")
        reiniciarCapacidadNaves()
        naveActual.guardarAlmacenamiento()

    canvas.moveto(puntero, lista[cont].getX()-4, lista[cont].getY()-4)
    return

#Ventana
ventana = Tk()
ventana.geometry("600x600")
ventana.title("Proyecto Datos")
Button(ventana, text="Generar sistema", foreground="white", background="black",  padx=5, pady=5, command=generarSistema, font=('Helvetica', 9, 'bold')).pack()
Button(ventana, text="Recolectar", foreground="white", background="black", padx=5, pady=5, font=('Helvetica', 9, 'bold'), command=enviarNaves).pack()
Button(ventana, text="Destruir", foreground="white", background="black", padx=5, pady=5, font=('Helvetica', 9, 'bold')).pack()
Button(ventana, text="Ver arbol de materiales", foreground="white", background="black", padx=5, pady=5, font=('Helvetica', 9, 'bold')).pack()

#Gráfico
canvas = Canvas(ventana, width=550, height=400, bg='gray')
canvas.pack(expand=YES)
canvas.create_oval(0,0, 40, 40, fill="gray", tags=['puntero'])
# canvas.create_oval(40,0, 80, 40, fill="red", tags=['puntero2'])
# canvas.create_oval(80,0, 120, 40, fill="green", tags=['puntero3'])
canvas.create_text(50, 80, text="U/ en el almacén: 0")
canvas.create_text(50, 100, text="Arbol de materiales: 0 nodos act.")


mainloop()