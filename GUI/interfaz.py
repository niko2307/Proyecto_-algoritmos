import tkinter as tk
from tkinter import messagebox
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tablero import crear_tablero, colocar_leopardo
from logica_juego import turno_vacas, vacas_ganan
from Algoritmo import minimax
from utils import hash_tablero

CELL_SIZE = 80

class JuegoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Las Vacas y el Leopardo - Interfaz Mejorada")
        self.root.configure(bg='#1e1e1e')

        self.canvas = tk.Canvas(
            self.root, 
            width=8*CELL_SIZE, 
            height=8*CELL_SIZE,
            bg="#2c2c2c",
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20)

        self.label_turno = tk.Label(
            self.root, 
            text="Turno actual: 🐆 Leopardo", 
            font=("Helvetica", 14), 
            fg="#fff", bg="#1e1e1e"
        )
        self.label_turno.pack()

        self.label_info = tk.Label(
            self.root, 
            text="", 
            font=("Helvetica", 12), 
            fg="#aaa", bg="#1e1e1e"
        )
        self.label_info.pack(pady=5)

        self.boton_turno = tk.Button(
            self.root, 
            text="▶ Siguiente Turno", 
            command=self.jugar_turno,
            font=("Helvetica", 14, "bold"),
            bg="#444", fg="#fff", activebackground="#666", activeforeground="#fff",
            relief=tk.RAISED, borderwidth=3
        )
        self.boton_turno.pack(pady=10)

        self.tablero = crear_tablero()
        self.pos_leopardo = colocar_leopardo(self.tablero, 3, 1)
        self.turno = 0  # 0 = leopardo, 1 = vacas
        self.historial = {}
        self.num_turno = 1

        self.dibujar_tablero()

    def dibujar_tablero(self, highlight=None):
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                x1, y1 = j*CELL_SIZE, i*CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = "#3e3e3e" if (i + j) % 2 == 0 else "#1e1e1e"

                if highlight and (i, j) == highlight:
                    color = "#3a6f3a"  # casilla objetivo destacada

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#555")

                pieza = self.tablero[i][j]
                if pieza == 'V':
                    self.canvas.create_text(
                        (x1+x2)//2, (y1+y2)//2, 
                        text="🐄",
                        font=("Segoe UI Emoji", 32)
                    )
                elif pieza == 'L':
                    self.canvas.create_text(
                        (x1+x2)//2, (y1+y2)//2, 
                        text="🐆",
                        font=("Segoe UI Emoji", 34, "bold")
                    )

    def jugar_turno(self):
        if self.pos_leopardo[0] == 7:
            messagebox.showinfo("🏆 Victoria", "El LEOPARDO ha ganado (llegó a la fila 7)!")
            return
        elif vacas_ganan(self.tablero, self.pos_leopardo):
            messagebox.showinfo("🐄 Derrota", "Las VACAS han ganado (acorralaron al leopardo)!")
            return

        if self.turno == 0:
            self.label_turno.config(text=f"Turno {self.num_turno}: 🐆 Leopardo")
            self.label_info.config(text="Calculando mejor movimiento...")
            self.root.update()
            time.sleep(0.8)

            _, mejor_mov = minimax(self.tablero, self.pos_leopardo, profundidad=4, maximizando=True)
            if mejor_mov:
                self.dibujar_tablero(highlight=mejor_mov)
                self.label_info.config(text=f"Leopardo se moverá a: {mejor_mov}")
                self.root.update()
                time.sleep(1.5)
                fila_old, col_old = self.pos_leopardo
                fila_new, col_new = mejor_mov
                self.tablero[fila_old][col_old] = '.'
                self.tablero[fila_new][col_new] = 'L'
                self.pos_leopardo = mejor_mov
            self.turno = 1

        else:
            self.label_turno.config(text=f"Turno {self.num_turno}: 🐄 Vacas")
            self.label_info.config(text="Las vacas se mueven...")
            self.root.update()
            turno_vacas(self.tablero, self.pos_leopardo)
            self.turno = 0
            self.num_turno += 1

        estado = hash_tablero(self.tablero)
        self.historial[estado] = self.historial.get(estado, 0) + 1
        if self.historial[estado] >= 3:
            messagebox.showinfo("🤝 Empate", "Se repitió el mismo estado 3 veces.")
            return

        self.dibujar_tablero()
        self.label_info.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoGUI(root)
    root.mainloop()