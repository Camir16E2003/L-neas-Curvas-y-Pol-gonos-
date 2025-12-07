import tkinter as tk
import math
from tkinter import simpledialog, messagebox

class AplicacionDibujo:
    def __init__(self, root):
        self.root = root   
        self.root.title("Practica 1: Líneas, Curvas y Polígonos")
        self.root.geometry("800x600")

        self.modo = tk.StringVar(value="Nada")
        self.puntos = []
        self.lados_poligono = 5

        #Interfaz de navegacion
        frame_controles = tk.Frame(root, bg="#ddd", pady=5)
        frame_controles.pack(side=tk.TOP, fill=tk.X)
        
        btn_linea = tk.Button(frame_controles, text="Lineas", command=self.modo_linea)
        btn_linea.pack(side=tk.LEFT, padx=5)

        btn_multilinea = tk.Button(frame_controles, text="Lineas sucesivas", command=self.modo_multilinea)
        btn_multilinea.pack(side=tk.LEFT, padx=5)

        btn_poligono = tk.Button(frame_controles, text="Poligonos (N lados)", command=self.modo_poligonos)
        btn_poligono.pack(side=tk.LEFT, padx=5)

        btn_limpiar = tk.Button(frame_controles, text="Limpiar pizarron", command=self.limpiar, bg="#e42121", fg="white")
        btn_limpiar.pack(side=tk.LEFT, padx=5)

        self.canvas = tk.Canvas(root, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.detectar_click)

    def modo_linea(self):
        self.modo.set("linea")
        self.puntos = []
    
    def modo_multilinea(self):
        self.modo.set("multilinea")
        self.puntos = []    

    def modo_poligonos(self):
        try:
            n = simpledialog.askinteger("Input", "¿Numero de lados?", minvalue=3, maxvalue=100)
            if n:
                self.lados_poligono = n
                self.modo.set("poligono")
                self.puntos = []
        except:
            pass
    
    def limpiar(self):
        self.canvas.delete("all")
        self.puntos = []
        self.modo.set("nada")

    def detectar_click(self, event):
        x, y = event.x, event.y
        modo_actual = self.modo.get()

        if modo_actual == "linea":
            self.puntos.append((x, y))
            if len(self.puntos) == 1:
                self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")
            elif len(self.puntos) == 2:
                x1, y1 = self.puntos[0]
                self.canvas.create_line(x1, y1, x, y, width=2, fill="black")
                self.puntos = []

        elif modo_actual == "multilinea":
            self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="red")
            self.puntos.append((x, y))
            if len(self.puntos) > 1:
                x_prev, y_prev = self.puntos[-2]
                self.canvas.create_line(x_prev, y_prev, x, y, width=2, fill="blue")

        elif modo_actual == "poligono":
            radio = 50
            self.dibujar_poligono(x, y, self.lados_poligono, radio)

    def dibujar_poligono(self, cx, cy, n, r):
        coords = []
        angulo_paso = (2 * math.pi) / n
        for i in range(n):
            angulo = i * angulo_paso - (math.pi / 2)
            px = cx + r * math.cos(angulo)
            py = cy + r * math.sin(angulo)
            coords.append(px)
            coords.append(py)
        self.canvas.create_polygon(coords, outline="green", fill="", width=2)
        self.canvas.create_oval(cx-2, cy-2, cx+2, cy+2, fill="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionDibujo(root)
    root.mainloop()