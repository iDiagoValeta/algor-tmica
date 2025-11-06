# -*- coding: utf-8 -*-
import re
from distancias_parte2 import *

class SpellSuggester:

    """
    Clase que implementa el método suggest para la búsqueda de términos.
    """

    def __init__(self,
                 dist_functions,
                 vocab = [],
                 default_distance = None,
                 default_threshold = None):
        
        """Método constructor de la clase SpellSuggester

        Construye una lista de términos únicos (vocabulario),

        Args:
           dist_functions es un diccionario nombre->funcion_distancia
           vocab es una lista de palabras o la ruta de un fichero
           default_distance debe ser una clave de dist_functions
           default_threshold un entero positivo

        """
        self.distance_functions = dist_functions
        self.set_vocabulary(vocab)
        if default_distance is None:
            default_distance = 'levenshtein'
        if default_threshold is None:
            default_threshold = 3
        self.default_distance = default_distance
        self.default_threshold = default_threshold

    def build_vocabulary(self, vocab_file_path):
        """Método auxiliar para crear el vocabulario.

        Se tokeniza por palabras el fichero de texto,
        se eliminan palabras duplicadas y se ordena
        lexicográficamente.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tokenizer (re.Pattern): expresión regular para la tokenización.
        """
        tokenizer=re.compile(r"\W+")
        with open(vocab_file_path, "r", encoding="utf-8") as fr:
            vocab = set(tokenizer.split(fr.read().lower()))
            vocab.discard("")  # por si acaso
            return sorted(vocab)

    def set_vocabulary(self, vocabulary):
        if isinstance(vocabulary,list):
            self.vocabulary = vocabulary # atención! nos quedamos una referencia, a tener en cuenta
        elif isinstance(vocabulary,str):
            self.vocabulary = self.build_vocabulary(vocabulary)
        else:
            raise Exception("SpellSuggester incorrect vocabulary value")

    def suggest(self, term, distance=None, threshold=None, flatten=True):
        """

        Args:
            term (str): término de búsqueda.
            distance (str): nombre del algoritmo de búsqueda a utilizar
            threshold (int): threshold para limitar la búsqueda
        """
        # Asignar valores por defecto si no se proporcionan
        if distance is None:
            distance = self.default_distance
        if threshold is None:
            threshold = self.default_threshold

        # Obtener la función de distancia correcta del diccionario (importado de distancias_parte2)
        dist_func = opcionesSpell[distance]

        # Crear una lista de listas para agrupar resultados por distancia.
        # resul[i] contendrá todas las palabras a distancia 'i'.
        resul = [[] for _ in range(threshold + 1)]

        # Iterar por cada palabra en el vocabulario pre-cargado
        for word in self.vocabulary:
            # Calcular la distancia (las funciones optimizadas pararán si > threshold)
            dist = dist_func(term, word, threshold)

            # Si la distancia es válida (menor o igual al umbral), añadirla a su grupo
            if dist <= threshold:
                # Se añade como lista [word] para cumplir el formato que espera el test
                resul[dist].append([word])

        # Si flatten es True, convertir la lista de listas de listas a una lista simple de palabras
        if flatten:
            # Comprensión de lista anidada para aplanar la estructura
            resul = [word for dist_list in resul for word_list in dist_list for word in word_list]
            
        return resul