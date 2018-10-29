import sys




def lee_fichero_imprenta(nombreFichero):
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

def optimiza_folletos(n, panfletos):
    def papel_nuevo(j):
        papel=[]
        for i in range(0, j):
            papel.append([0]*j)

        for i in range(0, n):
            for j in range(0, n):
                papel[i][j]=0
        return papel

    def comprobarHueco(i,j,anchura, altura, matrix):
        if(i+altura>=n or j+anchura>n):
            return False
        for comp_i in range(i, i + altura):
            for comp_j in range(j, j + anchura):
                print(matrix[comp_i][comp_i], matrix[comp_i][comp_i]!=0)
                if(matrix[comp_i][comp_i]!=0):
                    return False
        print("SI QUE CABE EN PAPEL")
        return True


    def posicionPapel(id, anchura, altura, matrix):
        for i in range(0, n):
            for j in range (0, n):
                if (comprobarHueco(i, j,anchura, altura, matrix)):
                    for marcar_i in range(i, i + altura):
                        for marcar_j in range(j, j + anchura):
                            matrix[marcar_i][marcar_j]=id
                            print(marcar_i, marcar_j)
                            return (i,j)
        return (-1,-1)
    hojas = list()
    hojas.append(papel_nuevo(n))
    sol = list()
    for folleto in panfletos:
          for id_hoja, papel in enumerate(hojas):
                print(id_hoja)
                pos = posicionPapel(folleto[0], folleto[1], folleto[2], papel)
                if (pos==(-1,-1)):
                    hoja = papel_nuevo(n)
                    hojas.append(hoja)
                    pos = posicionPapel(folleto[0], folleto[1], folleto[2], hoja)
                    PosicionFolleto = (folleto[0], hojas.index(hoja), pos[0], pos[1])
                    sol.append(PosicionFolleto)
                    break

                else:

                    PosicionFolleto = (folleto[0], id_hoja+1, pos[0], pos[1])
                    sol.append(PosicionFolleto)
                    break
    return sol

if __name__=="__main__":
    fichero = sys.argv[1]
    contenido = lee_fichero_imprenta(fichero)
    print(optimiza_folletos(contenido[0], contenido[1]))

