from utils import movimientos_leopardo, mover_leopardo, obtener_movimientos_vacas, mover_vaca ,hash_tablero
import copy

#funcion para evaluar el tablero  y mirar las posciciones de leopardo 
def evaluar_tablero(tablero, pos_leopardo):
    fila, col = pos_leopardo
    movs = movimientos_leopardo(tablero, fila, col)

    
    if fila == 7:
        return 10000
    if not movs:
        return -10000


    avance_score = fila * 1000  # Cuanto más cerca de 7, mejor

   
    libertad = len(movs) * 20


    amenaza = 0
    for i in range(8):
        for j in range(8):
            if tablero[i][j] == 'V':
                dist = abs(i - fila) + abs(j - col)
                if dist <= 3:
                    amenaza += 50 - dist * 10  # más cerca, más amenaza

   
    estancado = -100 if fila < 3 else 0

    return avance_score + libertad - amenaza + estancado
    
#funcion de implementacion del algoritmo minimax     

def minimax(tablero, pos_leopardo, profundidad, maximizando, historial=None):
    if historial is None:
        historial = set()

    estado_actual = hash_tablero(tablero)
    if estado_actual in historial:
        return -500, None  # penalizar repeticiones

    historial.add(estado_actual)

    if profundidad == 0 or evaluar_tablero(tablero, pos_leopardo) in [10000, -10000]:
        return evaluar_tablero(tablero, pos_leopardo), None

    if maximizando:
        mejor_valor = float('-inf')
        mejor_movimiento = None
        for mov in movimientos_leopardo(tablero, *pos_leopardo):
            nuevo_tablero = copy.deepcopy(tablero)
            nueva_pos = mover_leopardo(nuevo_tablero, pos_leopardo, mov)
            valor, _ = minimax(nuevo_tablero, nueva_pos, profundidad - 1, False, historial)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = mov
        return mejor_valor, mejor_movimiento
    else:
        peor_valor = float('inf')
        for vaca, movs in obtener_movimientos_vacas(tablero):
            for destino in movs:
                nuevo_tablero = copy.deepcopy(tablero)
                mover_vaca(nuevo_tablero, vaca, destino)
                valor, _ = minimax(nuevo_tablero, pos_leopardo, profundidad - 1, True, historial)
                if valor < peor_valor:
                    peor_valor = valor
        return peor_valor, None
