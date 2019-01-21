import sys
from typing import Tuple, List

Folleto = Tuple[int, int, int]  # (num_folleto, anchura, altura)
PosicionFolleto = Tuple[int, int, int, int]  # (num_folleto, num_hoja, pos_x ,pos_y)


def lee_fichero_imprenta(nombre_fichero: str) -> Tuple[int, List[Folleto]]:
    pf = []
    with open(nombre_fichero) as f:
        m = int(f.readline())
        for line in f:
            numf, anchura, altura = (int(i) for i in line.split())
            pf.append((numf, anchura, altura))
    return m, pf


def optimiza_folletos(n: int, panfletos: List[Folleto]) -> List[PosicionFolleto]:

    papeles = []  # CONTIENE LAS HOJAS USADAS
    res = []      # CONTIENE LA LISTA DE PosicionFolleto QUE SE DEVOLVERA

    def crear_papel():
        parte_papel = (0, 0, n, n)  # CREA UN TROZO PARA EL PAPEL IGUAL DE GRANDE QUE EL MAXIMO DE UN PAPEL
        papel = list()
        papel.append(parte_papel)
        papeles.append(papel)

    def add_folleto(num_folleto, anchura, altura):
        for papel in papeles:
            entrado = False
            for parte in papel:

                anchura_parte = parte[2] - parte[0]  # ANCHURA DEL FOLLETO
                altura_parte = parte[3] - parte[1]  # ALTURA DEL FOLLETO

                # ENTRA SI EL FOLLETO CABE EN EL TROZO DE PAPEL
                if anchura_parte >= anchura and altura_parte >= altura:

                    # AÑADE LA SOLUCIÓN A LA LISTA DE SOLUCIONES
                    res.append((num_folleto, papeles.index(papel) + 1, parte[0], parte[1]))

                    # EL FOLLETO OCUPA EN ANCHURA EL TROZO DE PAPEL, SE CREA UN TROZO DE PAPEL DEBAJO
                    if anchura_parte == anchura and altura_parte != altura:
                        papel.append((parte[0], parte[1] + altura, parte[2], parte[3]))

                    # EL FOLLETO OCUPA EN ALTURA EL TROZO DE PAPEL, SE CREA UN TROZO A SU LADO
                    elif altura_parte == altura and anchura_parte != anchura:
                        papel.append((parte[0] + anchura, parte[1], parte[2], parte[3]))

                    # EL FOLLETO NO CUBRE NI EN ALTURA NI ANCHURA EL TROZO DE PAPEL, SE CREAN AMBOS TROZOS
                    elif altura_parte != altura and anchura_parte != anchura:
                        papel.append((parte[0], parte[1] + altura, parte[0] + anchura, parte[3]))
                        papel.append((parte[0] + anchura, parte[1], parte[2], parte[3]))

                    papel.remove(parte)  # SE ELIMINA LA PARTE DE PAPEL ANTERIOR A LA INSERCION DEL FOLLETO
                    entrado = True
                    break

                else:
                    # SI SE ENCUENTRA EN EL ULTIMO PAPEL Y NO ENCUENTRA SITIO PARA EL FOLLETO, CREA UN NUEVO PAPEL
                    if papel.index(parte) + 1 == len(papel) and papeles.index(papel) + 1 == len(papeles):
                        crear_papel()

            if entrado:
                break

    crear_papel()

    # ORDENA LOS FOLLETOS DE MAS GRANDES A MAS PEQUEÑOS
    indices_ordenados = sorted(range(len(panfletos)), key=lambda n: -panfletos[n][1] - panfletos[n][2])

    for ind in indices_ordenados:
        folleto = panfletos[ind]
        add_folleto(folleto[0], folleto[1], folleto[2])

    return res


def muestra_solucion(sol: List[PosicionFolleto]):
    for i in range(0, len(sol)):
        print(sol[i][0], sol[i][1], sol[i][2], sol[i][3])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: imprenta.py <fichero_imprenta.txt>")
        exit(-1)
    fichero = sys.argv[1]
    contenido = lee_fichero_imprenta(fichero)
    sol = optimiza_folletos(contenido[0], contenido[1])
    muestra_solucion(sol)
