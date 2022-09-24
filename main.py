from tkinter import *
from modelos.Arbol import Arbol
from modelos.Nodo import Nodo
from modelos.JSON import JSON

arbolSistema = Arbol()
arbolMateriales = Arbol()

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
        canvas.create_text(i["textX"], i["textY"]+15, text=i["cantidad"], font=('Helvetica', 9, 'bold'))
    
        codigo = i["codigo"]
        nombre = i["nombre"]
        material = i["material"]
        cantidad = i["cantidad"]
        x = i["posicionX1"]
        y = i["posicionX2"]
        x2 = i["posicionX2"]
        y2 = i["posicionY2"]

        arbolSistema.agregar(Nodo(codigo, nombre, material, cantidad, x, y, x2, y2))
        
    print( arbolSistema.mostrarInOrden(arbolSistema.getRaiz()) )

#Ventana
ventana = Tk()
ventana.geometry("500x500")
Button(ventana, text="Generar sistema", foreground="white", background="black",  padx=5, pady=5, command=generarSistema, font=('Helvetica', 9, 'bold')).pack()
Button(ventana, text="Recolectar", foreground="white", background="black", padx=5, pady=5, font=('Helvetica', 9, 'bold')).pack()
#Gráfico
canvas = Canvas(ventana, width=400, height=400, bg='gray')
canvas.pack(expand=YES)

mainloop()