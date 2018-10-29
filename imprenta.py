import sys




def lee_fichero_imprenta(nombreFichero: str):
    folletos=list()
    f = open(nombreFichero, 'r')
    pLinea=True
    for linea in f.readlines():
        if pLinea==True:
            m=int(linea)
            pLinea=False
        else:
            linea = linea.split('\n')
            info = linea[0].split(' ')
            folleto = (int(info[0]), int(info[1]), int(info[2])) #(num_folleto, anchura, altura)
            folletos.append(folleto)
    contenido = (m, folletos)
    return contenido

def optimiza_folletos(n: int, panfletos: list(tuple())):
    def papel_nuevo(n: int):
        M=[]
        for i in range(0, n):
            M.append([0]*n)
        return M
    print(papel_nuevo(n))
    return None

if __name__=="__main__":
    fichero = sys.argv[1]
    contenido = lee_fichero_imprenta(fichero)
    optimiza_folletos(contenido[0], contenido[1])

