import sys
from time import time

from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo

from labyrinthviewer import LabyrinthViewer


def load_labyrinth(fichero):
    start_time = time()
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
        print('CAMINO CORTO CON PARED: ', pesoCamino)
        pesoSP = pesoCamino
        pared = list()
        for i in range(0, filas):
            for j in range(0, nColumnas):
                if(i+1<=filas-1):
                    spOpcional = matriz[i][j] + mInversa[i + 1][j]
                    if (spOpcional < pesoCamino and spOpcional < pesoSP and (i + 1, j) not in grafo.succs((i, j))):
                        pesoSP = matriz[i][j] + mInversa[i+1][j] + 1 #+1 po el paso extra de pasar la pared
                        print(pesoSP)
                        pared = [(i, j), (i + 1, j)]
                if (j + 1 <= nColumnas - 1):
                    spOpcional = matriz[i][j] + mInversa[i][j+1]
                    if (spOpcional < pesoCamino and spOpcional < pesoSP and (i, j+1) not in grafo.succs((i, j))):
                        pesoSP = matriz[i][j] + mInversa[i][j+1] + 1 #+1 por el paso extra de pasar la pared
                        print(pesoSP)
                        pared = [(i, j), (i, j+1)]
        return pared

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
    print(mInversa)
    print(matriz)
    print(paredes)
    #vertices = recorrido_aristas_anchura(grafo, (0, 0))
    #verticesFinal = recorrido_aristas_anchura(grafo, (filas-1, columnas-1))

    recorrido_corto = recuperador_camino(inicio, (filas - 1, columnas - 1))
    elapsed_time = time() - start_time
    print("Tiempo de ejecucion: %.10f segundos." % elapsed_time)
    lv = LabyrinthViewer(grafo, canvas_width=600, canvas_height=400, margin=10)
    lv.add_path(recorrido_corto, color="blue")
    #lv.run()

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


    # print("Número de argumentos con los que has llamado al programa:", len(sys.argv))
    # print("El nombre del programa:", sys.argv[0])
    # for argumento in sys.argv[1:]:
    # print(argumento)

    graph = load_labyrinth('pruebas/laberinto-15x24.i')
    # vertices = recorrido_aristas_anchura(graph, (0,0))
    # recorrido = path(graph, (0, 0), (9, 19))
    # recorrido_corto = shortest_path(graph, (0, 0), (9, 19))
    # lv = LabyrinthViewer(graph, canvas_width=600, canvas_height=400, margin=10)
    # lv.add_path(recorrido, color="blue")
    # lv.add_path(recorrido_corto, color="red")
    # lv.run()

