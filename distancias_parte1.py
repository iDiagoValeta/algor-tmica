######################################################################
#
# INTEGRANTES DEL EQUIPO/GRUPO:
#
# - Adrián Gimeno Bernat - 21791624K
# - Carlos Ruiz úbeda    - 44895499M
# - Jaime Moreno Vicente - 21790058E
# - Ignacio Diago Valeta - 45904832Y
#
######################################################################


import numpy as np

def levenshtein_matriz(x, y):
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=np.int32)
    for i in range(1, lenX + 1):
        D[i][0] = D[i - 1][0] + 1
    for j in range(1, lenY + 1):
        D[0][j] = D[0][j - 1] + 1
        for i in range(1, lenX + 1):
            D[i][j] = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + (x[i - 1] != y[j - 1]),
            )
    return D[lenX, lenY]


######################################################################
                        # EJERCICIO 1
######################################################################


def levenshtein_edicion(x, y):
    # Parte 1: Calcular la matriz de distancias.
    # Esta parte es similar a la función levenshtein_matriz proporcionada.
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=int)

    for i in range(1, lenX + 1):
        D[i][0] = i
    for j in range(1, lenY + 1):
        D[0][j] = j

    for i in range(1, lenX + 1):
        for j in range(1, lenY + 1):
            coste_sustitucion = 0 if x[i - 1] == y[j - 1] else 1
            
            D[i][j] = min(
                D[i - 1][j] + 1,                      # BorradO.
                D[i][j - 1] + 1,                      # Inserción.
                D[i - 1][j - 1] + coste_sustitucion   # Sustitución o acierto.
            )

    # Parte 2: Recuperar la secuencia de operaciones (Backtracking).
    # Se parte desde la esquina inferior derecha y se retrocede hacia el origen.
    edicion = []
    i, j = lenX, lenY

    while i > 0 or j > 0:
        # El coste de la operación diagonal (0 si hay acierto, 1 si hay sustitución)
        coste_sustitucion = 0 if i > 0 and j > 0 and x[i-1] == y[j-1] else 1

        # Se prioriza el camino diagonal si es el que da el coste mínimo.
        # Esto corresponde a una sustitución o un acierto.
        if i > 0 and j > 0 and D[i][j] == D[i-1][j-1] + coste_sustitucion:
            operacion = (x[i-1], y[j-1])
            edicion.append(operacion)
            i -= 1
            j -= 1
        # Si no, se comprueba el camino desde la izquierda, que corresponde a una inserción.
        elif j > 0 and D[i][j] == D[i][j-1] + 1:
            operacion = ('', y[j-1])
            edicion.append(operacion)
            j -= 1
        # Si no, se comprueba el camino desde arriba, que corresponde a un borrado.
        elif i > 0 and D[i][j] == D[i-1][j] + 1:
            operacion = (x[i-1], '')
            edicion.append(operacion)
            i -= 1
        else:
            # Si la matriz está bien construida, no debería llegar aquí.
            break

    # La secuencia se obtiene en orden inverso, por lo que se le da la vuelta.
    edicion.reverse()
    
    # Se devuelve la distancia final y la lista de operaciones.
    return D[lenX, lenY], edicion


######################################################################
                        # EJERCICIO 2
######################################################################


def damerau_restricted_matriz(x, y):
    # Creamos la matriz auxiliar para ejecutar el algoritmo.
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=int)

    # Inicialización de la primera fila y columna, que representan inserciones y borrados.
    for i in range(1, lenX + 1):
        D[i][0] = i
    for j in range(1, lenY + 1):
        D[0][j] = j

    # Relleno del resto de la matriz.
    for i in range(1, lenX + 1):
        for j in range(1, lenY + 1):
            # Coste de sustitución: 0 si los caracteres son iguales, 1 si son diferentes.
            coste_sustitucion = 0 if x[i - 1] == y[j - 1] else 1
            
            # Se calcula el mínimo entre borrado, inserción y sustitución.
            D[i][j] = min(
                D[i - 1][j] + 1,                         # Borrado.
                D[i][j - 1] + 1,                         # Inserción.
                D[i - 1][j - 1] + coste_sustitucion      # Sustitución o acierto.
            )
            
            # Se añade el caso de la transposición, según la fórmula de la versión restringida.
            if i > 1 and j > 1 and x[i - 1] == y[j - 2] and x[i - 2] == y[j - 1]:
                D[i][j] = min(D[i][j], D[i - 2][j - 2] + 1) # Transposición

    # La distancia final se encuentra en la esquina inferior derecha de la matriz.
    return D[lenX, lenY]


######################################################################
                        # EJERCICIO 3
######################################################################


def damerau_restricted_edicion(x, y):
    # Parte 1: Calcular la matriz de distancias (igual que en damerau_restricted_matriz).
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=int)

    for i in range(1, lenX + 1):
        D[i][0] = i
    for j in range(1, lenY + 1):
        D[0][j] = j

    for i in range(1, lenX + 1):
        for j in range(1, lenY + 1):
            coste_sustitucion = 0 if x[i - 1] == y[j - 1] else 1
            
            D[i][j] = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + coste_sustitucion
            )
            
            if i > 1 and j > 1 and x[i - 1] == y[j - 2] and x[i - 2] == y[j - 1]:
                D[i][j] = min(D[i][j], D[i - 2][j - 2] + 1)

    # Parte 2: Recuperar la secuencia de operaciones (Backtracking).
    edicion = []
    i, j = lenX, lenY

    while i > 0 or j > 0:
        # Se prioriza la operación de transposición, ya que es la condición más específica.
        if i > 1 and j > 1 and x[i-1] == y[j-2] and x[i-2] == y[j-1] and D[i][j] == D[i-2][j-2] + 1:
            operacion = (x[i-2:i], y[j-2:j]) # Formato ('ab', 'ba')
            edicion.append(operacion)
            i -= 2
            j -= 2
        else:
            coste_sustitucion = 0 if i > 0 and j > 0 and x[i-1] == y[j-1] else 1
            
            # Se comprueba si el camino proviene de una sustitución/acierto.
            if i > 0 and j > 0 and D[i][j] == D[i-1][j-1] + coste_sustitucion:
                operacion = (x[i-1], y[j-1])
                edicion.append(operacion)
                i -= 1
                j -= 1
            # Se comprueba si proviene de un borrado.
            elif i > 0 and D[i][j] == D[i-1][j] + 1:
                operacion = (x[i-1], '')
                edicion.append(operacion)
                i -= 1
            # Finalmente, se asume que proviene de una inserción (podríamos insertar un elif y luego un "else: break" también).
            else: # j > 0 and D[i][j] == D[i][j-1] + 1.
                operacion = ('', y[j-1])
                edicion.append(operacion)
                j -= 1

    # Las operaciones se obtienen en orden inverso, por lo que es necesario revertir la lista.
    edicion.reverse()

    # La distancia final se encuentra en la esquina inferior derecha de la matriz.
    return D[lenX, lenY], edicion


######################################################################
                        # EJERCICIO 4
######################################################################


def damerau_intermediate_matriz(x, y):
    # Creamos la matriz auxiliar para ejecutar el algoritmo.
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=int)

    # Inicialización de la primera fila y columna.
    for i in range(1, lenX + 1):
        D[i][0] = i
    for j in range(1, lenY + 1):
        D[0][j] = j

    # Relleno del resto de la matriz.
    for i in range(1, lenX + 1):
        for j in range(1, lenY + 1):
            # 1. Costes de las operaciones básicas (Levenshtein).
            coste_sustitucion = 0 if x[i - 1] == y[j - 1] else 1
            D[i][j] = min(
                D[i - 1][j] + 1,                      # Borrado.
                D[i][j - 1] + 1,                      # Inserción.
                D[i - 1][j - 1] + coste_sustitucion   # Sustitución o acierto.
            )
            
            # 2. Condición de la versión restringida (coste 1).
            if i > 1 and j > 1 and x[i - 1] == y[j - 2] and x[i - 2] == y[j - 1]:
                D[i][j] = min(D[i][j], D[i - 2][j - 2] + 1) # Transposición.
            
            # 3. Nuevas condiciones de la versión intermedia (coste 2).
            # Caso acb -> ba.
            if i > 2 and j > 1 and x[i-1] == y[j-2] and x[i-3] == y[j-1]:
                D[i][j] = min(D[i][j], D[i-3][j-2] + 2)
            
            # Caso ab -> bca.
            if i > 1 and j > 2 and x[i-2] == y[j-1] and x[i-1] == y[j-3]:
                 D[i][j] = min(D[i][j], D[i-2][j-3] + 2)

    # La distancia final se encuentra en la esquina inferior derecha de la matriz.
    return D[lenX, lenY]


######################################################################
                        # EJERCICIO 5
######################################################################


def damerau_intermediate_edicion(x, y):
    # Parte 1: Calcular la matriz de distancias (igual que en damerau_intermediate_matriz).
    lenX, lenY = len(x), len(y)
    D = np.zeros((lenX + 1, lenY + 1), dtype=int)

    for i in range(1, lenX + 1):
        D[i][0] = i
    for j in range(1, lenY + 1):
        D[0][j] = j

    for i in range(1, lenX + 1):
        for j in range(1, lenY + 1):
            coste_sustitucion = 0 if x[i - 1] == y[j - 1] else 1
            D[i][j] = min(
                D[i - 1][j] + 1,
                D[i][j - 1] + 1,
                D[i - 1][j - 1] + coste_sustitucion
            )
            if i > 1 and j > 1 and x[i-1] == y[j-2] and x[i-2] == y[j-1]:
                D[i][j] = min(D[i][j], D[i-2][j-2] + 1)
            if i > 2 and j > 1 and x[i-1] == y[j-2] and x[i-3] == y[j-1]:
                D[i][j] = min(D[i][j], D[i-3][j-2] + 2)
            if i > 1 and j > 2 and x[i-2] == y[j-1] and x[i-1] == y[j-3]:
                D[i][j] = min(D[i][j], D[i-2][j-3] + 2)

    # Parte 2: Recuperar la secuencia de operaciones (Backtracking).
    edicion = []
    i, j = lenX, lenY

    while i > 0 or j > 0:
        # Se comprueban primero las operaciones más complejas.
        # Caso ab -> bca.
        if i > 1 and j > 2 and x[i-2] == y[j-1] and x[i-1] == y[j-3] and D[i][j] == D[i-2][j-3] + 2:
            operacion = (x[i-2:i], y[j-3:j])
            edicion.append(operacion)
            i -= 2
            j -= 3
        # Caso acb -> ba.
        elif i > 2 and j > 1 and x[i-1] == y[j-2] and x[i-3] == y[j-1] and D[i][j] == D[i-3][j-2] + 2:
            operacion = (x[i-3:i], y[j-2:j])
            edicion.append(operacion)
            i -= 3
            j -= 2
        # Caso ab -> ba (restringido).
        elif i > 1 and j > 1 and x[i-1] == y[j-2] and x[i-2] == y[j-1] and D[i][j] == D[i-2][j-2] + 1:
            operacion = (x[i-2:i], y[j-2:j])
            edicion.append(operacion)
            i -= 2
            j -= 2
        else:
            # Operaciones básicas de Levenshtein.
            coste_sustitucion = 0 if i > 0 and j > 0 and x[i-1] == y[j-1] else 1
            if i > 0 and j > 0 and D[i][j] == D[i-1][j-1] + coste_sustitucion:
                operacion = (x[i-1], y[j-1])
                edicion.append(operacion)
                i -= 1
                j -= 1
            elif i > 0 and D[i][j] == D[i-1][j] + 1:
                operacion = (x[i-1], '')
                edicion.append(operacion)
                i -= 1
            else:
                operacion = ('', y[j-1])
                edicion.append(operacion)
                j -= 1
                
    # Las operaciones se obtienen en orden inverso, por lo que es necesario revertir la lista.
    edicion.reverse()

    # La distancia final se encuentra en la esquina inferior derecha de la matriz.
    return D[lenX, lenY], edicion


######################################################################
                        # RESTO DEL ARCHIVO
######################################################################

    
opcionesSpell = {
    'levenshtein_m': levenshtein_matriz,
    'damerau_rm':    damerau_restricted_matriz,
    'damerau_im':    damerau_intermediate_matriz,
}

opcionesEdicion = {
    'levenshtein': levenshtein_edicion,
    'damerau_r':   damerau_restricted_edicion,
    'damerau_i':   damerau_intermediate_edicion
}

if __name__ == "__main__":
    print(levenshtein_matriz("ejemplo", "campos"))
