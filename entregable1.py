import sys

from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo

from labyrinthviewer import LabyrinthViewer


def load_labyrinth(fichero):
    def recorrido_anchura(grafo: "Graph<T>", v_inicial: "T", inversa: "bool") -> "List<(T,T)>":
        aristas = []
        queue = Fifo()
        seen = set()
        queue.push((v_inicial, v_inicial))
        seen.add(v_inicial)
        matriz[0][0]=0
        mInversa[0][0]=0
        while len(queue) > 0:
            u, v = queue.pop()
            aristas.append((u, v))
            #peso=len(recuperador_camino(aristas, v))-1
            if(inversa):
                peso = mInversa[v[0]][v[1]]
            else:
                peso = matriz[v[0]][v[1]]
            for suc in grafo.succs(v):
                if suc not in seen:
                    if (inversa):
                        mInversa[suc[0]][suc[1]] = peso + 1
                        seen.add(suc)
                        queue.push((v, suc))
                    else:
                        matriz[suc[0]][suc[1]] = peso + 1
                        seen.add(suc)
                        queue.push((v, suc))
        return aristas

    def buscarPared(grafo: "Graph<T>")-> "List<(T,T)>":
        pesoCamino = matriz[filas-1][nColumnas-1]
        pesoSP = pesoCamino
        paredes = list()
        for i in range(0, filas):
            for j in range(0, nColumnas):
                if(i+1<=filas-1):
                    spOpcional = matriz[i][j] + mInversa[i + 1][j]
                    if (spOpcional < pesoCamino and spOpcional < pesoSP and (i + 1, j) not in grafo.succs((i, j))):
                        pesoSP = matriz[i][j] + mInversa[i+1][j] + 1 #+1 po el paso extra de pasar la pared
                        if (pesoSP > spOpcional):
                            paredes.clear()
                            paredes.append([(i, j), (i + 1, j)])
                        else:
                            if(pesoSP == spOpcional):
                                paredes.append([(i, j), (i + 1, j)])
                if (j+1 <= nColumnas - 1):
                    spOpcional = matriz[i][j] + mInversa[i][j+1]+1
                    if (spOpcional < pesoCamino and spOpcional < pesoSP and (i, j+1) not in grafo.succs((i, j))):
                        pesoSP = matriz[i][j] + mInversa[i][j+1] + 1 #+1 por el paso extra de pasar la pared
                        if (pesoSP > spOpcional):
                            paredes.clear()
                            paredes.append([(i, j), (i, j+1)])
                        else:
                            if(pesoSP == spOpcional):
                                paredes.append([(i, j), (i, j+1)])

        while(len(paredes)!=1):
            if(paredes[0][0][0] != paredes[1][0][0] or paredes[0][1][0] != paredes[1][1][0]):
                if(paredes[0][0][0]==paredes[1][0][0]):
                    if(paredes[0][1][0] != paredes[1][1][0]):
                        if (paredes[0][1][0] > paredes[1][1][0]):
                            paredes.pop(0)
                        else:
                            paredes.pop(1)
                else:
                    if (paredes[0][0][0] < paredes[1][0][0]):
                        paredes.pop(0)
                    else:
                        paredes.pop(1)
            else:

                if (paredes[0][0][1]<paredes[1][0][1]):
                    paredes.pop(1)
                else:
                    paredes.pop(0)
        print(paredes[0][0][0], paredes[0][0][1],paredes[0][1][0],paredes[0][1][1])
        print(pesoCamino)
        print(pesoSP)
        return paredes

    f = open(fichero, 'r')
    pasillos = []
    filas = 0
    for linea in f.readlines():
        celdas = linea.split(',')
        nColumnas = len(celdas)
        columnas = 0
        for celda in celdas:
            if 'w' not in celda:
                pasillos.append(((filas, columnas), (filas, columnas - 1)))
            if 'e' not in celda:
                pasillos.append(((filas, columnas), (filas, columnas + 1)))
            if 'n' not in celda:
                pasillos.append(((filas, columnas), (filas - 1, columnas)))
            if 's' not in celda:
                pasillos.append(((filas, columnas), (filas + 1, columnas)))
            columnas += 1
        filas += 1
    f.close()
    # GRAFO
    grafo = UndirectedGraph(E=pasillos)
    mInversa = []
    for i in range(0, filas):
        mInversa.append([0] * nColumnas)
    matriz = []
    for i in range(0, filas):
        matriz.append([0] * nColumnas)
    inicio = recorrido_anchura(grafo, (0,0), False)
    fin = recorrido_anchura(grafo, (filas - 1, columnas - 1), True)
    paredes = buscarPared(grafo)

    if (grafico):
        recorrido_inicio = recuperador_camino(inicio, (paredes[0][0][0], paredes[0][0][1]))
        recorrido_fin = recuperador_camino(fin, (paredes[0][1][0], paredes[0][1][1]))
        lv = LabyrinthViewer(grafo, canvas_width=600, canvas_height=400, margin=10)
        lv.add_path(recorrido_inicio, color="red")
        lv.add_path(recorrido_fin, color="red")
        lv.add_marked_cell((paredes[0][0][0], paredes[0][0][1]),color="red")
        lv.add_marked_cell((paredes[0][1][0], paredes[0][1][1]),color="red")
        lv.run()

    return grafo

def recuperador_camino(lista_aristas: "List<(T,T)>", v: "T") -> "List<T>":
        # Crea un dicionario de punteros hacia atrás (backpointers)
        bp = {}
        for o, d in lista_aristas:
            bp[d] = o
        # Reconstruye el camino yendo hacia atrás
        camino = []
        camino.append(v)
        while v != bp[v]:
            v = bp[v]
            camino.append(v)
        # Invierte el camino pues lo hemos obtenido al revés
        camino.reverse()
        return camino



def shortest_path(lab: "Graph<T>", source: "T", target: "T") -> "T | None":
    vertices = recorrido_aristas_anchura(lab, source)
    return recuperador_camino(vertices, target)


def recorrido_aristas_anchura(grafo: "Graph<T>", v_inicial: "T") -> "List<(T,T)>":
    aristas = []
    queue = Fifo()
    seen = set()
    queue.push((v_inicial, v_inicial))
    seen.add(v_inicial)
    while len(queue) > 0:
        u, v = queue.pop()
        aristas.append((u, v))
        for suc in grafo.succs(v):
            if suc not in seen:
                seen.add(suc)
                queue.push((v, suc))
    return aristas


if __name__ == "__main__":
    fichero = sys.argv[1]
    if(len(sys.argv)==3):
        grafico=True
    else:
        grafico=False
    grafo = load_labyrinth(fichero)


