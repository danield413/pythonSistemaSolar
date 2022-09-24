from tkinter import *
import threading

from modelos.Saludo import Saludo
Grafica = Tk()

Grafica.geometry("400x400")
Grafica.configure(bg="#BFFFFF")
Grafica.title("Hola mundo")

tinfo1 = Text(Grafica, width=15, height=8)
tinfo1.pack(side=LEFT)
tinfo2 = Text(Grafica, width=15, height=8)
tinfo2.pack(side=RIGHT)
tinfo3 = Text(Grafica, width=15, height=8)
tinfo3.pack(side=TOP)

proceso1 = Saludo("CARLOS")
proceso2 = Saludo("DANIEL")
proceso3 = Saludo("FIGUE")

h1 = threading.Thread(target=proceso1.saludar, args=('hilo1', tinfo1))
h2 = threading.Thread(target=proceso2.saludar, args=('hilo2', tinfo2))
h3 = threading.Thread(target=proceso3.saludar, args=('hilo3', tinfo3))

h1.start()
h2.start()
h3.start()

Grafica.mainloop()