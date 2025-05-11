
# funcion para definir ,los movimientops validos para el leopardo 
def movimientos_leopardo(tablero, x, y):
    direcciones = [(-2, -2), (-2, 2), (2, -2), (2, 2)]  # diagonales dobles
    movimientos = []

    for dx, dy in direcciones:
        nx, ny = x + dx, y + dy
        mx, my = x + dx // 2, y + dy // 2  # casilla intermedia

        if (
            0 <= nx < 8 and 0 <= ny < 8 and      # destino válido
            tablero[nx][ny] == '.' and           # destino vacío
            tablero[mx][my] == '.'               # intermedio vacío también
        ):
            movimientos.append((nx, ny))

    return movimientos



# funcion para mover el leopardo dentro del tablero 
def mover_leopardo(tablero, origen, destino):
    ox, oy = origen
    dx, dy = destino
    tablero[ox][oy] = '.'
    tablero[dx][dy] = 'L'
    return (dx, dy)

# funcion para validar los moviminetos de las vacas 
def movimientos_vaca(tablero, x, y):
    movimientos = []
    direcciones = [(-1, -1), (-1, 1)]  # solo hacia adelante
    for dx, dy in direcciones:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 8 and 0 <= ny < 8 and tablero[nx][ny] == '.':
            movimientos.append((nx, ny))
    return movimientos

#funcion para hacer los moviminetos de las vacas 
def mover_vaca(tablero, origen, destino):
    ox, oy = origen
    dx, dy = destino
    tablero[ox][oy] = '.'
    tablero[dx][dy] = 'V'

#funcion parea encontrar las vacas y los moviminetos 
def obtener_movimientos_vacas(tablero):
    vacas = []
    for i in range(8):
        for j in range(8):
            if tablero[i][j] == 'V':
                movs = movimientos_vaca(tablero, i, j)
                if movs:
                    vacas.append(((i, j), movs))
    return vacas   


# funcion para guardar lo estados del tablero 

def hash_tablero(tablero):
    return ''.join(''.join(fila) for fila in tablero)