import tkinter as tk
from tkinter import messagebox
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tablero import crear_tablero, colocar_leopardo
from logica_juego import turno_leopardo, turno_vacas, vacas_ganan
from utils import hash_tablero

CELL_SIZE = 60

class JuegoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Las Vacas y el Leopardo")

        self.canvas = tk.Canvas(self.root, width=8*CELL_SIZE, height=8*CELL_SIZE)
        self.canvas.pack()

        self.boton_turno = tk.Button(self.root, text="Siguiente Turno", command=self.jugar_turno)
        self.boton_turno.pack(pady=10)

        self.tablero = crear_tablero()
        self.pos_leopardo = colocar_leopardo(self.tablero, 3, 1)
        self.turno = 0  # 0 = leopardo, 1 = vacas
        self.historial = {}

        self.dibujar_tablero()

    def dibujar_tablero(self):
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                x1, y1 = j*CELL_SIZE, i*CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = "#EEE" if (i + j) % 2 == 0 else "#BBB"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                pieza = self.tablero[i][j]
                if pieza == 'V':
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="🐄", font=("Arial", 24))
                elif pieza == 'L':
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="🐆", font=("Arial", 24))

    def jugar_turno(self):
        if self.pos_leopardo[0] == 7:
            messagebox.showinfo("Victoria", "🏆 El LEOPARDO ha ganado (llegó a la fila 7)!")
            return
        elif vacas_ganan(self.tablero, self.pos_leopardo):
            messagebox.showinfo("Derrota", "🐄 Las VACAS han ganado (acorralaron al leopardo)!")
            return

        if self.turno == 0:
            self.pos_leopardo = turno_leopardo(self.tablero, self.pos_leopardo)
            self.turno = 1
        else:
            turno_vacas(self.tablero, self.pos_leopardo)
            self.turno = 0

        # Detección de ciclos (empate)
        estado = hash_tablero(self.tablero)
        self.historial[estado] = self.historial.get(estado, 0) + 1
        if self.historial[estado] >= 3:
            messagebox.showinfo("Empate", "🤝 Se repitió el mismo estado 3 veces.")
            return

        self.dibujar_tablero()


# Punto de entrada
if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoGUI(root)
    root.mainloop()