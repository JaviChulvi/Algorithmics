import sys
import time
from typing import Tuple, List

Folleto = Tuple[int, int, int]               # (num_folleto, anchura, altura)
PosicionFolleto = Tuple[int, int, int, int]  # (num_folleto, num_hoja, pos_x ,pos_y)


def lee_fichero_imprenta(nombreFichero: str) -> Tuple[int , List[Folleto]]:
    pf = []
    with open(nombreFichero) as f:
        m = int(f.readline())
        for line in f:
            numf, anchura, altura = (int(i) for i in line.split())
            pf.append((numf, anchura, altura))
    return m, pf

def optimiza_folletos(n: int, panfletos: List[Folleto]) -> List[PosicionFolleto]:
    # PartePapel = (x_inicio, y_inicio, x_fin, y_fin) -- Papel = list(PartePapel) -- papeles = list(Papel)

    def crear_Papel():
        parte_papel = (0,0,n,n) # CREA UN TROZO PARA EL PAPEL IGUAL DE GRANDE QUE EL MAXIMO DE UN PAPEL
        papel = list()
        papel.append(parte_papel)
        papeles.append(papel)

    def addFolleto(id, anchura, altura):
        for papel in papeles:
            entrado = False
            for parte in papel:

                anchura_parte = parte[2] - parte[0] # ANCHURA DEL FOLLETO
                altura_parte = parte[3] - parte[1] # ALTURA DEL FOLLETO

                if(anchura_parte >=anchura and altura_parte>=altura): # ENTRA SI EL FOLLETO CABE EN EL TROZO DE PAPEL
                    sol.append((id, papeles.index(papel)+1, parte[0],parte[1])) # AÑADE LA SOLUCIÓN A LA LISTA DE SOLUCIONES
                    if (anchura_parte == anchura and altura_parte != altura): # EL FOLLETO OCUPA EN ANCHURA EL TROZO DE PAPEL
                        papel.append((parte[0], parte[1] + altura, parte[2], parte[3])) # SE CREA UN TROZO DE PAPEL DEBAJO DEL FOLLETO
                    elif (altura_parte == altura and anchura_parte != anchura): # EL FOLLETO OCUPA EN ALTURA EL TROZO DE PAPEL
                        papel.append((parte[0] + anchura, parte[1], parte[2], parte[3])) #SE CREA UN TROZO A SU LATERAL
                    elif (altura_parte != altura and anchura_parte != anchura): # EL FOLLETO NO CUBRE NI EN ALTURA NI ANCHURA NI ALTURA EL TROZO DE PAPEL
                        papel.append((parte[0], parte[1] + altura, parte[0] + anchura, parte[3]))  # SE CREA UN TROZO DE PAPEL A SU LATERAL Y OTRO DEBAJO DE EL
                        papel.append((parte[0] + anchura, parte[1], parte[2], parte[3]))
                    papel.remove(parte) # SE ELIMINA LA PARTE DE PAPEL ANTERIOR A LA INSERCION DEL FOLLETO
                    entrado = True
                    break
                else:
                    if(papel.index(parte)+1==len(papel) and papeles.index(papel)+1==len(papeles)): # SI SE ENCUENTRA EN EL ULTIMO PAPEL Y NO ENCUENTRA SITIO PARA EL FOLLETO CREA UN NUEVO PAPEL
                        crear_Papel()
            if(entrado):
                break

    papeles = list()
    sol = list()
    crear_Papel()

    indices_ordenados = sorted(range(len(panfletos)), key=lambda n: -panfletos[n][1] - panfletos[n][2]) # ORDENA LOS FOLLETOS DE MAS GRANDES A MAS PEQUEÑOS

    for ind in indices_ordenados:
        folleto = panfletos[ind]
        addFolleto(folleto[0], folleto[1], folleto[2])

    return sol

def muestra_solucion(sol: List[PosicionFolleto]):
    for i in range(0 , len(sol)):
        print(sol[i][0],sol[i][1],sol[i][2],sol[i][3])

if __name__=="__main__":
    fichero = sys.argv[1]
    contenido = lee_fichero_imprenta(fichero)
    sol = optimiza_folletos(contenido[0], contenido[1])
    f = open("solucion.txt", "w")
    for i in range(0 , len(sol)):
        f.write(str(sol[i][0])+ " " + str(sol[i][1])+ " " + str(sol[i][2])+ " " + str(sol[i][3]) +"\n")
    muestra_solucion(sol)

