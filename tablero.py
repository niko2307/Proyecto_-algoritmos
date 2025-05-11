
# funcion de creacion del tablero en la ultima ilera del tablero 
def crear_tablero():
    tablero = [['.' for _ in range(8)] for _ in range(8)]
    for col in range(1, 8, 2):  # vacas en columnas impares
        tablero[7][col] = 'V'
    return tablero

# funcion para hacer la impresion  del tablero fila por fila
def imprimir_tablero(tablero):
    print("\n   " + ' '.join(str(col) for col in range(8)))  # encabezado de columnas
    for fila in range(8):
        print(f"{fila}  " + ' '.join(tablero[fila][col] for col in range(8)))



#funcion para  colocar al leopardo dentro del tablero 
def colocar_leopardo(tablero, fila=3, col=1):
    tablero[fila][col] = 'L'
    return (fila, col)  # posición actual del leopardo
