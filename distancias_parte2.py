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

from collections import Counter
import numpy as np

def levenshtein_matriz(x, y, threshold=None):
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

def levenshtein_reduccion(x, y, threshold=None):
    """
        Calcula la distancia de Levenshtein usando solo dos vectores columna.
    """
    lenX, lenY = len(x), len(y)

    vprev = np.zeros(lenX + 1, dtype=np.int32)
    vcurrent = np.zeros(lenX + 1, dtype=np.int32)

    # Inicializamos vprev
    for i in range(lenX + 1):
        vprev[i] = i

    # Iteramos para calcular el resto de columnas
    for j in range(1, lenY + 1):
        vcurrent[0] = j # Primer elemento de la columna actual

        # Calculamos el resto de elementos de la columna actual
        for i in range(1, lenX + 1):
            deletion_cost = vcurrent[i - 1] + 1 # Coste de borrado

            insertion_cost = vprev[i] + 1 # Coste de inserción

            coste_letra = 0 if x[i - 1] == y[j - 1] else 1
            substitution_cost = vprev[i - 1] + coste_letra # Coste de sustitución

            # El mínimo de las tres operaciones es el que aplicamos
            vcurrent[i] = min(deletion_cost, insertion_cost, substitution_cost)

        # La columna actual (vcurrent) se convierte en la previa (vprev)
        vprev, vcurrent = vcurrent, vprev

    # La distancia total está en el último elemento de vprev al final del bucle
    return vprev[lenX]

def levenshtein(x, y, threshold):
    """
        - Calcula la distancia de Levenshtein pero con parada temprana por threshold.
        - Pararemos el cálculo tan pronto como sepamos que la distancia seguro superará el umbral.
    """
    lenX, lenY = len(x), len(y)

    # Si la diferencia de longitud es mayor que el umbral,
    # la distancia de Levenshtein nunca puede ser menor o igual.
    if abs(lenX - lenY) > threshold:
        return threshold + 1

    vprev = np.zeros(lenX + 1, dtype=np.int32)
    vcurrent = np.zeros(lenX + 1, dtype=np.int32)

    for i in range(lenX + 1):
        vprev[i] = i

    for j in range(1, lenY + 1):
        vcurrent[0] = j

        # Mínimo de la columna actual
        min_dist_en_columna = j

        for i in range(1, lenX + 1):
            deletion_cost = vcurrent[i - 1] + 1

            insertion_cost = vprev[i] + 1

            coste_letra = 0 if x[i - 1] == y[j - 1] else 1
            substitution_cost = vprev[i - 1] + coste_letra

            vcurrent[i] = min(deletion_cost, insertion_cost, substitution_cost)

            # Actualizamos el mínimo de esta columna si es necesario
            if vcurrent[i] < min_dist_en_columna:
                min_dist_en_columna = vcurrent[i]

        # Si el valor más bajo en la columna que acabamos de calcular ya supera el umbral, paramos.
        if min_dist_en_columna > threshold:
            return threshold + 1

        vprev, vcurrent = vcurrent, vprev

    final_dist = vprev[lenX]

    # Si al final es mayor, devolvemos threshold+1
    if final_dist > threshold:
        return threshold + 1
    else:
        return final_dist

def levenshtein_cota_optimista(x, y, threshold):
    """
        - Calcula la cota optimista (bag of characters).
        - Si la cota supera el threshold, devuelve threshold + 1.
        - Si no, delega en la función levenshtein para el cálculo real.
    """
    # Recorre 'x' y suma 1 por cada caracter
    conteo_x = Counter(x)
    # Recorre 'y' y resta 1 por cada caracter
    conteo_x.subtract(Counter(y))

    # conteo_x tiene el balance de caracteres

    suma_positivos = 0
    suma_negativos = 0

    # Sumar valores extra en 'x' e 'y'
    for v in conteo_x.values():
        if v > 0:
            suma_positivos += v
        elif v < 0:
            suma_negativos += v

    cota = max(suma_positivos, abs(suma_negativos))

    # Si la cota ya es mayor, ahorramos el cálculo
    if cota > threshold:
        return threshold + 1

    # Si la cota es válida, llamamos a la función Levenshtein
    return levenshtein(x, y, threshold)

def damerau_restricted(x, y, threshold):
    # versión con reducción coste espacial y parada por threshold
    lenX, lenY = len(x), len(y)

    if abs(lenX - lenY) > threshold:
        return threshold + 1

    vprev2 = np.zeros(lenX + 1, dtype=np.int32)
    vprev1 = np.zeros(lenX + 1, dtype=np.int32)
    vcurrent = np.zeros(lenX + 1, dtype=np.int32)

    for i in range(lenX + 1):
        vprev1[i] = i

    for j in range(1, lenY + 1):
        vcurrent[0] = j
        min_dist_en_columna = j

        for i in range(1, lenX + 1):
            
            # Lógica de Levenshtein
            coste_letra = 0 if x[i - 1] == y[j - 1] else 1
            
            borrado = vcurrent[i - 1] + 1
            insercion = vprev1[i] + 1
            sustitucion = vprev1[i - 1] + coste_letra

            vcurrent[i] = min(borrado, insercion, sustitucion)

            # Lógica de Damerau-Restringida
            if i > 1 and j > 1 and x[i - 1] == y[j - 2] and x[i - 2] == y[j - 1]:
                # Coste = D[i-2, j-2] + 1
                coste_transposicion = vprev2[i - 2] + 1
                vcurrent[i] = min(vcurrent[i], coste_transposicion)
            
            # Actualizamos el mínimo de la columna
            if vcurrent[i] < min_dist_en_columna:
                min_dist_en_columna = vcurrent[i]

        # Parada por Threshold
        if min_dist_en_columna > threshold:
            return threshold + 1
        
        # Rotamos los vectores
        vprev2, vprev1, vcurrent = vprev1, vcurrent, vprev2

    final_dist = vprev1[lenX]

    if final_dist > threshold:
        return threshold + 1
    else:
        return final_dist

def damerau_intermediate(x, y, threshold):
    # versión con reducción coste espacial y parada por threshold
    lenX, lenY = len(x), len(y)

    if abs(lenX - lenY) > threshold:
        return threshold + 1

    vprev3 = np.zeros(lenX + 1, dtype=np.int32)
    vprev2 = np.zeros(lenX + 1, dtype=np.int32)
    vprev1 = np.zeros(lenX + 1, dtype=np.int32)
    vcurrent = np.zeros(lenX + 1, dtype=np.int32)

    for i in range(lenX + 1):
        vprev1[i] = i

    for j in range(1, lenY + 1):
        vcurrent[0] = j
        min_dist_en_columna = j

        for i in range(1, lenX + 1):
            
            # Lógica de Levenshtein
            coste_letra = 0 if x[i - 1] == y[j - 1] else 1
            borrado = vcurrent[i - 1] + 1
            insercion = vprev1[i] + 1
            sustitucion = vprev1[i - 1] + coste_letra
            vcurrent[i] = min(borrado, insercion, sustitucion)

            # Lógica de Damerau-Restringida
            if i > 1 and j > 1 and x[i - 1] == y[j - 2] and x[i - 2] == y[j - 1]:
                coste_transposicion = vprev2[i - 2] + 1 # D[i-2, j-2] + 1
                vcurrent[i] = min(vcurrent[i], coste_transposicion)
            
            # Lógica de Damerau-Intermedia
            if i > 2 and j > 1 and x[i-1] == y[j-2] and x[i-3] == y[j-1]:
                coste_intermedio_1 = vprev2[i-3] + 2 # D[i-3, j-2] + 2
                vcurrent[i] = min(vcurrent[i], coste_intermedio_1)

            if i > 1 and j > 2 and x[i-2] == y[j-1] and x[i-1] == y[j-3]:
                coste_intermedio_2 = vprev3[i-2] + 2 # D[i-2, j-3] + 2
                vcurrent[i] = min(vcurrent[i], coste_intermedio_2)

            # Actualizamos el mínimo de la columna
            if vcurrent[i] < min_dist_en_columna:
                min_dist_en_columna = vcurrent[i]

        # Parada por Threshold
        if min_dist_en_columna > threshold:
            return threshold + 1
        
        # Rotamos los vectores
        vprev3, vprev2, vprev1, vcurrent = vprev2, vprev1, vcurrent, vprev3

    final_dist = vprev1[lenX]

    if final_dist > threshold:
        return threshold + 1
    else:
        return final_dist

opcionesSpell = {
    'levenshtein_m': levenshtein_matriz,
    'levenshtein_r': levenshtein_reduccion,
    'levenshtein':   levenshtein,
    'levenshtein_o': levenshtein_cota_optimista,
    'damerau_r':     damerau_restricted,
    'damerau_i':     damerau_intermediate
}

if __name__ == "__main__":
    print(levenshtein_matriz("ejemplo", "campos"))