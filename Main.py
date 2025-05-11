import time
from tablero import crear_tablero, imprimir_tablero, colocar_leopardo
from logica_juego import leopardo_gana, vacas_ganan, turno_leopardo, turno_vacas
from utils import hash_tablero

def main():
    tablero = crear_tablero()
    pos_leopardo = colocar_leopardo(tablero, 3, 1)

    turno = 0  # 0 = leopardo, 1 = vacas
    estado_repetido = {}  # Para detectar ciclos infinitos

    while True:
        print("\n--- Estado actual del tablero ---")
        imprimir_tablero(tablero)

        # primero verificar si ganó el leopardo
        if pos_leopardo[0] == 7:  # llegó a la fila de las vacas
            print("\n🏆 El LEOPARDO ha ganado (llegó a la fila 7)!")
            break
        elif vacas_ganan(tablero, pos_leopardo):
            print("\n🐄 Las VACAS han ganado (acorralaron al leopardo)!")
            break

        if turno == 0:
            print("\nTurno del LEOPARDO")
            pos_leopardo = turno_leopardo(tablero, pos_leopardo)
            turno = 1
        else:
            print("\nTurno de las VACAS")
            turno_vacas(tablero, pos_leopardo)
            turno = 0

        #  Detección de repetición de estado
        estado_actual = hash_tablero(tablero)
        estado_repetido[estado_actual] = estado_repetido.get(estado_actual, 0) + 1

        if estado_repetido[estado_actual] >= 3:
            print("\n🤝 EMPATE: se repitió el mismo estado 3 veces.")
            break

        time.sleep(1.5)



if __name__ == "__main__":
    main()
