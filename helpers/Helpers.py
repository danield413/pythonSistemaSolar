from abc import abstractmethod
import random
from tkinter import *
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk


""" Clase Helpers que ayuda a la reutilización de código """
class Helpers:
    def __init__(self):
        pass

    """
        Retorna el nodo del arbol de materiales que tenga el codigo que se le pasa por parametro
        
        :param arbolMateriales: el arbol de materiales
        :param codigo: el codigoAsignado del material
        :return: el nodo del arbol de materiales 
    """
    def getNodoMaterialPorCodigo(arbolMateriales, codigo):
        arbolMateriales.resetLista()
        for nodo in arbolMateriales.mostrarInOrden(arbolMateriales.getRaiz()):
            if nodo.getDato() == codigo:
                return nodo
        return None

    """
        Genera un número aleatorio entre 0 y 1000
        :return: el número aleatorio.
    """
    @abstractmethod
    def generarCodigoAlmacenajeMaterial() -> int:
        return random.randint(0, 1000)

    
    """
        Genera un número aleatorio entre 1 y 3, y luego devuelve una lista de planetas en el orden de
        el número aleatorio (InOrden, PreOrden o PostOrden)
        
        :param nave: la instancia de la Nave
        :param arbolSistema: el arbol de planetas
        :return: la lista de planetas en el orden aleatorio (InOrden, PreOrden o PostOrden)
    """
    @abstractmethod
    def generarRecorrido(nave, arbolSistema) -> list:
        numeroRandom = random.randint(1, 3)
        # print(">> Nave:", nave.getNumero(), "- Recorrido asignado => ", numeroRandom)
        recorrido = []
        arbolSistema.resetLista()
        if numeroRandom == 1:
            recorrido = arbolSistema.mostrarInOrden(arbolSistema.getRaiz())
        if numeroRandom == 2:
            recorrido = arbolSistema.mostrarPreOrden(arbolSistema.getRaiz())
        if numeroRandom == 3:
            recorrido = arbolSistema.mostrarPostOrden(arbolSistema.getRaiz())
        return recorrido

    """
        Resetea los valores de las naves.
        
        :param naves: la lista de las 3 naves
        :param canvas: el gráfico canvas donde se muestra la aplicación
    """
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

        canvas.itemconfig("naveActual", text="Nave: ")
        canvas.itemconfig("oro", text="Oro: 0")
        canvas.itemconfig("plata", text="Plata: 0")
        canvas.itemconfig("bronce", text="Bronce: 0")
        canvas.moveto("nave", 40, 20)

    """
        Se encarga de recorrer todos los planetas y ejecutar el método aumentarCantidad
        el cuál hace que cada 10 segundos aumente 2 unidades de material
        
        :param canvas: el gráfico canvas donde se muestra la aplicación
        :param arbolSistema: el arbol de planetas
    """
    @abstractmethod
    def generarMateriales(canvas, arbolSistema):
        arbolSistema.resetLista()
        nodos = arbolSistema.mostrarInOrden(arbolSistema.getRaiz())
        for i in nodos:
            i.aumentarCantidad(canvas)

    """
        Devuelve el planeta (Nodo) identificado por el código
        
        :param numero: el número (Código) del planeta
        :param arbolSistema: el arbol de planetas
        :return: el Nodo del planeta
    """
    @abstractmethod
    def getNodoPorCodigo(numero, arbolSistema):
        arbolSistema.resetLista()
        planetas = arbolSistema.mostrarInOrden(arbolSistema.getRaiz())
        for i in planetas:
            if i.getDato() == numero:
                return i
        return None

    """
        Devuelve el planeta (Nodo) identificado por el nombre
        
        :param nombre: el nombre del planeta
        :param arbolSistema: el arbol de planetas
        :return: el Nodo del planeta
    """
    @abstractmethod
    def getNodoPorNombre(nombre, arbolSistema):
        arbolSistema.resetLista()
        planetas = arbolSistema.mostrarInOrden(arbolSistema.getRaiz())
        for i in planetas:
            if i.getNombre() == nombre:
                return i
        return None

    """
        Dibuja el árbol de planetas en el gráfico canvas 
        con sus respectivos planetas y sus conexiones
        y los datos referentes a cada uno

        También dibuja datos extras como la información de la nave actual
        y la cantidad de material que tiene cada nave además de la cantidad de materiales 
        en el almacén y número de nodos en el árbol de materiales
        
        :param canvas: el gráfico canvas donde se muestra la aplicación
        :param arbolSistema: el arból de planetas
    """
    @abstractmethod
    def mostrarArbol(canvas, arbolSistema):

        canvas.delete("Pluton")
        canvas.delete("Mercurio")
        canvas.delete("Tarca")
        canvas.delete("Zulman")
        canvas.delete("Triton")
        canvas.delete("Zork")
        canvas.delete("Beltrak")
        canvas.delete("Yari")

        canvas.delete("planeta")
        canvas.delete("dato")
        canvas.delete("linea")
    
        canvas.create_text(
            40,
            60,
            text="Nave: ",
            tags=["naveActual"],
            font=("Helvetica", 9, "bold"),
            fill="white",
        )
        canvas.create_text(
            40,
            80,
            text="Oro: 0",
            tags=["oro"],
            font=("Helvetica", 10, "bold"),
            fill="white",
        )
        canvas.create_text(
            40,
            100,
            text="Plata: 0",
            tags=["plata"],
            font=("Helvetica", 10, "bold"),
            fill="white",
        )
        canvas.create_text(
            40,
            120,
            text="Bronce: 0",
            tags=["bronce"],
            font=("Helvetica", 10, "bold"),
            fill="white",
        )
        

        for i in arbolSistema.mostrarInOrden(arbolSistema.getRaiz()):
            color = ""
            if i.getMaterial() == "oro":
                color = "#BBA750"
            if i.getMaterial() == "plata":
                color = "#839D9E"
            if i.getMaterial() == "bronce":
                color = "#7B5F32"
            canvas.create_oval(i.getX(), i.getY(), i.getX2(), i.getY2(), fill=color, tags=["planeta"])
            nombre = "{0} - {1}".format(i.getNombre(), i.getDato())
            canvas.create_text(
                i.getX() + 10,
                i.getY2() + 15,
                text=nombre,
                font=("Helvetica", 9, "bold"),
                fill="white",
                tags="dato"
            )
            canvas.create_text(
                i.getX() + 10,
                i.getY2() + 30,
                text=i.getCantidad(),
                font=("Helvetica", 9, "bold"),
                tags=nombre,
                fill="white",
            )

        for i in arbolSistema.mostrarInOrden(arbolSistema.getRaiz()):
            if i.getIzquierda():
                canvas.create_line(
                    i.getX() + 15,
                    i.getY() + 15,
                    i.getIzquierda().getX() + 15,
                    i.getIzquierda().getY() + 15,
                    fill="red",
                    width=2,
                    tags=["linea"]
                )
            if i.getDerecha():
                canvas.create_line(
                    i.getX() + 15,
                    i.getY() + 15,
                    i.getDerecha().getX() + 15,
                    i.getDerecha().getY() + 15,
                    fill="blue",
                    width=2,
                    tags=["linea"]
                )

    """
        Toma el arbol de materiales y lo muestra en una nueva ventana y en un nuevo gráfico canvas
        
        :param arbolMateriales: el arbol de materiales
    """
    def mostrarArbolMateriales(materiales, canvasdos):
        print(">>>>>>>>>> Mostrar arbol de materiales")
        canvasdos.delete("all")

        for i in materiales:
            canvasdos.create_oval(
                i.getX(), i.getY(), i.getX2(), i.getY2(), fill=i.getColor(), tags=["nodomaterial"]
            )
            canvasdos.create_text(
                i.getTextX(), i.getY2() + 15, text=i.getDato(), fill=i.getTextColor(), tags=["textomaterial"]
            )

        for i in materiales:
            if i.getIzquierda():
                canvasdos.create_line(
                    i.getX() + 15,
                    i.getY() + 15,
                    i.getIzquierda().getX() + 15,
                    i.getIzquierda().getY() + 15,
                    fill="red",
                    width=2,
                    tags=["lineamaterial"]
                )
            if i.getDerecha():
                canvasdos.create_line(
                    i.getX() + 15,
                    i.getY() + 15,
                    i.getDerecha().getX() + 15,
                    i.getDerecha().getY() + 15,
                    fill="blue",
                    width=2,
                    tags=["lineamaterial"]
                )
    
    """
        Crea una ventana con un cuadro de texto y un botón. Cuando se pulsa el botón, se busca en el
        árbol el valor del cuadro de texto y muestra el resultado en la ventana
        
        :param arbolMateriales: el arbol de materiales
        """
    def buscarEnArbolMateriales(arbolMateriales):

        def buscar(entrada, ventana):
            nodo = Helpers.getNodoMaterialPorCodigo(arbolMateriales, int(entrada.get()))

            if(nodo != None):
                Label(ventana, text="Código asignado: " + str( nodo.getDato()) ).grid(row=1, column=0)
                Label(ventana, text="Material: " + str( nodo.getMaterial()) ).grid(row=2, column=0)
                Label(ventana, text="Cantidad: " + str( nodo.getCantidad()) ).grid(row=3, column=0)
                Label(ventana, text="Fecha: " + str( nodo.getFecha()) ).grid(row=4, column=0)

                arbolMateriales.resetLista()
            else:
                print("No se encontró el nodo.")

        root = Tk()
        root.title("Buscar en el árbol de materiales")
        root.geometry("400x200")
        codigo = tk.Entry()

        frame = Frame(root)
        frame.grid(row=0, column=0, padx=5, pady=5)

        label = Label(frame, text="Ingrese el código asignado del material que busca")
        label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="n")

        entrada = Entry(frame, width=30, textvariable=codigo)
        entrada.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        botonSubmit = Button(
            frame,
            text="Buscar",
            command=lambda: buscar(entrada, root)
        )

        botonSubmit.grid(row=2, column=1, sticky="e", padx=5, pady=5)

        root.mainloop()


    """
        Elimina un nodo del árbol de materiales
        
        :param arbolMateriales: el arból de materiales
        :param nodo: el nodo a eliminar
        :param canvasdos: el canvas donde se muestra el árbol de materiales
        :param canvasPrincipal: el canvas donde se muestra el árbol de sistema
    """
    def eliminar(arbolMateriales, nodo, canvasdos, canvasPrincipal):
        nodo = Helpers.getNodoMaterialPorCodigo(arbolMateriales, int(nodo))
        print(arbolMateriales.cantidadNodos(arbolMateriales.getRaiz()))
        arbolMateriales.eliminarNodo(nodo)
        print(arbolMateriales.cantidadNodos(arbolMateriales.getRaiz()))

        arbolMateriales.resetLista()
        Helpers.mostrarArbolMateriales(arbolMateriales.mostrarInOrden(arbolMateriales.getRaiz()), canvasdos)
        textoNodos = "Arb Mat. Nodos: " + str(
        arbolMateriales.cantidadNodos(arbolMateriales.getRaiz()))
        canvasPrincipal.itemconfig("nodosArbolMateriales", text=textoNodos)


    """
        Crea una ventana con un cuadro de texto y un botón. Cuando se pulsa el botón, se busca en el
        árbol el valor del cuadro de texto y muestra el arbol actualizado
        
        :param arbolMateriales: el arbol de materiales
        :param canvasdos: el canvas donde se muestra el arbol de materiales
        :param canvasPrincipal: el canvas donde se muestra el arbol del sistema
    """
    def eliminarNodoArbolMateriales(arbolMateriales, canvasdos, canvasPrincipal):
        root = Tk()
        root.title("Eliminar Nodo")
        root.geometry("400x200")

        labels = []
        arbolMateriales.resetLista()
        for i in arbolMateriales.mostrarInOrden(arbolMateriales.getRaiz()):
            if i.getDato() not in labels:
                labels.append(i.getDato())


        l1 = Label(root, text="Seleccione el nodo de material que desea eliminar: ")
        l1.pack()

        lista_desplegable = ttk.Combobox(root, width=20)
        lista_desplegable["values"] = labels
        lista_desplegable.pack()

        Button(root, text="eliminar", command=lambda: Helpers.eliminar(arbolMateriales, lista_desplegable.get(), canvasdos, canvasPrincipal)).pack()

        root.mainloop()   
        

    """
        Crea una ventana con un menu (eliminar y buscar) y muestra el arbol del sistema
        
        :param arbolMateriales: el arbol de materiales
        :param canvasPrincipal: el canvas donde se muestra el arbol del sistema
    """
    @abstractmethod
    def crearInterfazArbolMateriales(arbolMateriales, canvasPrincipal):
        arbolMateriales.resetLista()
        materiales = arbolMateriales.mostrarInOrden(arbolMateriales.getRaiz())
        ventanados = Tk()
        ventanados.geometry("600x600")
        ventanados.title("Arbol de materiales")
        canvasdos = Canvas(ventanados, width=550, height=600, bg="black")
        canvasdos.pack(expand=YES)

        barraMenu = Menu(ventanados)
        mnuBuscar = Button(barraMenu)
        mnuEliminar = Button(barraMenu)

        barraMenu.add_cascade(
            label="Buscar", menu=mnuBuscar, command=lambda: Helpers.buscarEnArbolMateriales(arbolMateriales)
        )
        barraMenu.add_cascade(
            label="Eliminar", menu=mnuEliminar, command=lambda: Helpers.eliminarNodoArbolMateriales(arbolMateriales, canvasdos, canvasPrincipal)
        )

        ventanados.config(menu=barraMenu)

        #carga los datos del arbol de materiales en el canvas
        Helpers.mostrarArbolMateriales(materiales, canvasdos)

        mainloop()