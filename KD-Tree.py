
from typing import *
from easycanvas import EasyCanvas
from kdtree import Axis, KDTree, KDNode, KDLeaf
import sys

def read_points(filename: str) -> List[Tuple[float, float]]:
    lista = list()
    with open(filename) as f:
        for i, linea in enumerate(f.readlines()):
            casillas = linea.strip().split(" ")
            lista.append((float(casillas[0]), float(casillas[1])))
    return lista

def build_kd_tree(points: List[Tuple[float, float]]) -> KDTree:
    if(len(points)==1):
        return KDLeaf(points[0])
    minimo0 = maximo0 = points[0][0]
    minimo1 = maximo1 = points[0][1]
    for point in points:
        if point[0] > maximo0:
            maximo0 = point[0]
        elif minimo0 > point[0]:
            minimo0 = point[0]
        if point[1] > maximo1:
            maximo1 = point[1]
        elif minimo1 > point[1]:
            minimo1 = point[1]
    diferencia0 = maximo0 - minimo0
    diferencia1 = maximo1 - minimo1
    if diferencia0 > diferencia1:
        indices_ordenados = sorted(points, key=lambda n: n[0])
        middle = len(indices_ordenados)//2
        if len(indices_ordenados)%2==0:
            mediana=(indices_ordenados[middle-1][0] +indices_ordenados[middle][0])/2
        else:
            mediana=indices_ordenados[middle][0]
        list0 = list()
        list1 = list()
        for point in points:
            if point[0] < mediana:
                list0.append(point)
            else:
                list1.append(point)
        return KDNode(0, mediana, build_kd_tree(list0), build_kd_tree(list1))
    else:
        indices_ordenados = sorted(points, key=lambda n: n[1])
        middle = len(indices_ordenados)//2
        if len(points)%2==0:
            mediana=(indices_ordenados[middle-1][1] +indices_ordenados[middle][1])/2
        else:
            mediana=indices_ordenados[middle][1]
        list0 = list()
        list1 = list()
        for point in points:
            if point[1] < mediana:
                list0.append(point)
            else:
                list1.append(point)
        return KDNode(1, mediana, build_kd_tree(list0), build_kd_tree(list1))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: entreable4.py <fichero_puntos.txt>")
        exit(-1)
    fichero = sys.argv[1]
    lista = read_points(fichero)
    tree = build_kd_tree(lista)
    print(tree.pretty())
