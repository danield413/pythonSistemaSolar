import random
import threading
import time
from tkinter import *
from modelos.Arbol import Arbol
from modelos.Nodo import Nodo
from modelos.JSON import JSON

arbolSistema = Arbol()

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
        arbolSistema.agregar(Nodo(codigo, nombre, material, cantidad, x, y, x2, y2))

    generarMateriales()

def enviarNaves():
    
        proceso1 = empezarARecolectar('puntero')
        proceso2 = empezarARecolectar('puntero2')
        proceso3 = empezarARecolectar('puntero3')

        hilo1 = threading.Thread(name="HiloNave1",target=proceso1)
        hilo2 = threading.Thread(name="HiloNave2",target=proceso2)
        hilo3 = threading.Thread(name="HiloNave3",target=proceso3)

        hilo1.start()
        hilo2.start()
        hilo3.start()

def empezarARecolectar(puntero):
    numeroRandom = random.randint(1,3)
    print("Número ", numeroRandom)
    recorrido = []
    arbolSistema.resetLista()
    if(numeroRandom == 1): recorrido = arbolSistema.mostrarInOrden(arbolSistema.getRaiz())
    if(numeroRandom == 2): recorrido = arbolSistema.mostrarPreOrden(arbolSistema.getRaiz())
    if(numeroRandom == 3): recorrido = arbolSistema.mostrarPostOrden(arbolSistema.getRaiz())
    recolectar(0, recorrido, len(recorrido)-1, puntero)

def recolectar(cont, lista, length, puntero):
    print(cont, length)
    if(cont <= length): 
        canvas.moveto(puntero, lista[cont].getX()-4, lista[cont].getY()-4)

    tarea = canvas.after(1000, recolectar, cont+1, lista, length, puntero)
    if(cont == length): 
        canvas.after_cancel(tarea)
        volver(puntero)
        return
        
def volver(puntero):
    if(puntero == "puntero"): canvas.moveto(puntero,40,0)
    if(puntero == "puntero2"): canvas.moveto(puntero,80,0)
    if(puntero == "puntero3"): canvas.moveto(puntero,120,0)
    

#Ventana
ventana = Tk()
ventana.geometry("500x500")
ventana.title("Proyecto Datos")
Button(ventana, text="Generar sistema", foreground="white", background="black",  padx=5, pady=5, command=generarSistema, font=('Helvetica', 9, 'bold')).pack()
Button(ventana, text="Recolectar", foreground="white", background="black", padx=5, pady=5, font=('Helvetica', 9, 'bold'), command=enviarNaves).pack()

#Gráfico
canvas = Canvas(ventana, width=400, height=400, bg='gray')
canvas.pack(expand=YES)
canvas.create_oval(0,0, 40, 40, fill="blue", tags=['puntero'])
canvas.create_oval(40,0, 80, 40, fill="red", tags=['puntero2'])
canvas.create_oval(80,0, 120, 40, fill="green", tags=['puntero3'])




mainloop()