from utils import (
    movimientos_leopardo,
    mover_leopardo,
    obtener_movimientos_vacas,
    mover_vaca
)

from Algoritmo import minimax

import random
import copy

#funcion para validar que gana el leopardo 
def leopardo_gana(pos_leopardo):
    fila, _ = pos_leopardo
    return fila == 0

# funcion para validar que las vacas ganan 
def vacas_ganan(tablero, pos_leopardo):
    return len(movimientos_leopardo(tablero, *pos_leopardo)) == 0

# funcion para validarel tuno del leopardo
#  tiene restriccion de no moverse si ya no encuentra mas casillas para moverse 
#implementa el algoritmo minimax , para el calculo del movimineto en el turno 
def turno_leopardo(tablero, pos_leopardo):
    _, mejor_mov = minimax(tablero, pos_leopardo, profundidad=4, maximizando=True)
    if mejor_mov:
        return mover_leopardo(tablero, pos_leopardo, mejor_mov)
    return pos_leopardo 


# funcion para el turno de las vacas 
# mirando los movimineto del tablero 
def turno_vacas(tablero, pos_leopardo):
    vacas_con_opciones = obtener_movimientos_vacas(tablero)
    leopardo_movs_1 = movimientos_leopardo(tablero, *pos_leopardo)

    # Predecir movimientos del siguiente turno (profundidad 2)
    leopardo_movs_2 = set()
    for nx, ny in leopardo_movs_1:
        leopardo_movs_2.update(movimientos_leopardo(tablero, nx, ny))

    posibles_destinos = set(leopardo_movs_1) | leopardo_movs_2

    # Barajar el orden para que no siempre se muevan las mismas primero
    random.shuffle(vacas_con_opciones)

    # Usamos un tablero copia para no alterar mientras se decide
    tablero_copy = copy.deepcopy(tablero)

    for (vx, vy), opciones in vacas_con_opciones:
        mejor_opcion = None
        mejor_score = float('-inf')

        for (nx, ny) in opciones:
            # Verificamos que el destino esté vacío en el tablero copiado
            if tablero_copy[nx][ny] != '.':
                continue

            # Calculamos valor del movimiento
            score = 0
            if (nx, ny) in posibles_destinos:
                score += 100  # bloqueo importante
            score -= abs(nx - pos_leopardo[0]) + abs(ny - pos_leopardo[1])

            if score > mejor_score:
                mejor_score = score
                mejor_opcion = (nx, ny)

        if mejor_opcion:
            mover_vaca(tablero, (vx, vy), mejor_opcion)
            tablero_copy[vx][vy] = '.'  # simula que la vaca se fue
            tablero_copy[mejor_opcion[0]][mejor_opcion[1]] = 'V'