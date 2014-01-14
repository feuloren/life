# -*- coding:utf-8 -*-

import numpy as np

class LifeComputer:
    def __init__(self, width, height):
        self.width = int(width)
        self.height = int(height)
        self.configure()
        self.handlers = []

    def set_size(self, width=None, height=None):
        """Définie la hauteur et/ou la largeur de la grille.
        Appelle les gestionnaires de changement d'état une fois terminé."""
        set = False

        if not(width is None) and int(width) != self.width:
            self.width = int(width)
            set = True

        if not(height is None) and int(height) != self.height:
            self.height = int(height)
            set = True

        if set:
            self.reconfigure()

    def configure(self):
        self.array = np.zeros((self.width+2, self.height+2), dtype=int)

    def reconfigure(self):
        self.configure()
        self.change()
        # TODO

    def compute_naive(self, iterations=1):
        """Calcul d'itérations débile.
        Appelle les gestionnaires de changement d'état une fois terminé."""
        for c in range(iterations):
            tmp = np.zeros((self.width, self.height), dtype=int)
            for i in range(self.width):
                for j in range(self.height):
                    tmp[i,j] = self.array[i,j] + self.array[i+1,j] + self.array[i+2,j] +\
                        self.array[i,j+1] + self.array[i+2,j+1] +\
                        self.array[i,j+2] + self.array[i+1,j+2] + self.array[i+2,j+2]

            for i in range(self.width):
                for j in range(self.height):
                    if self.array[i+1,j+1] == 0:
                        if tmp[i,j] == 3:
                            self.array[i+1,j+1] = 1
                        else:
                            self.array[i+1,j+1] = 0
                    else:
                        if tmp[i,j] == 2 or tmp[i,j] == 3:
                            self.array[i+1,j+1] = 1
                        else:
                            self.array[i+1,j+1] = 0
        self.change()

    def compute_less_naive(self, iterations=1):
        """Calcul d'itérations un peu plus optimisé.
        Appelle les gestionnaires de changement d'état une fois terminé."""
        for c in range(iterations):
            tmp = np.zeros(self.array.shape, dtype=int)
            for i in range(self.width):
                for j in range(self.height):
                    nb_voisins = self.array[i:i+3,j:j+3].sum() - self.array[i+1,j+1]

                    if self.array[i+1,j+1] == 1:
                        if nb_voisins == 3 or nb_voisins == 2:
                            tmp[i+1,j+1] = 1
                        else:
                            tmp[i+1,j+1] = 0
                    else:
                        if nb_voisins == 3:
                            tmp[i+1,j+1] = 1
                        else:
                            tmp[i+1,j+1] = 0

        self.array = tmp
        self.change()

    def compute(self, iterations=1):
        """Calcul d'itérations optimisé.
        Appelle les gestionnaires de changement d'état une fois terminé."""
        for c in range(iterations):
            # on récupère le nombre de voisins pour chaque élément
            neighbours = self.array[ :-2, :-2] + self.array[ :-2,1:-1] + self.array[ :-2,2:  ] +\
                self.array[1:-1, :-2]                         + self.array[1:-1,2:  ] +\
                self.array[2:  , :-2] + self.array[2:  ,1:-1] + self.array[2:  ,2:  ]
            
            # on calcule ceux qui vont naitre
            birth = (neighbours == 3) & (self.array[1:-1,1:-1] == 0)
            # et ceux qui ne vont PAS mourrir
            survive = ((neighbours == 2) | (neighbours == 3)) & (self.array[1:-1,1:-1] == 1)
            # on reset l'array
            self.array[...] = 0
            # et on met ceux qui sont vivants à 1
            self.array[1:-1,1:-1][birth | survive] = 1
        self.change()

    def fill_random(self):
        """Remplie aléatoirement la grille de cellules.
        Appelle les gestionnaires de changement d'état une fois terminé."""
        self.array[1:-1,1:-1] = np.random.random_integers(0, 1, (self.width, self.height))
        self.change()

    def reset(self):
        """Tue toutes les cellules de la grille"""
        self.array[...] = 0

    def translate_coordinates(self, coords):
        """Transforme les coordonnées utilisateur en coordonnées internes.
        Cela permet d'utiliser un array avec des 0 sur les bords mais de cacher
        ce bord à l'utilisateur"""
        if coords is Ellipsis: # On veut sélectionner tout (Ellipsis = ...)
            x, y = slice(1,-1), slice(1,-1)
        else:
            x, y = coords
            if isinstance(x, slice):
                x = slice(x.start +1, x.stop + 1, x.step) 
            else:
                x += 1
            if isinstance(y, slice):
                y = slice(y.start +1, y.stop + 1, y.step)
            else:
                y += 1

        return (x,y)

    def toggle(self, x, y):
        if self[x,y] == 1:
            self[x, y] = 0
        else:
            self[x, y] = 1

        self.change()

    def change(self):
        """Signale le changement d'état à tous les gestionnaires connectés"""
        for handler in self.handlers:
            handler(self)

    def connect_changed_handler(self, handler):
        """Ajoute un gestionnaire de changement d'état. Il sera appelé à chaque itération
        ou lorsque les propriétés du LifeComputer sont modifiées"""
        self.handlers.append(handler)

    def __getitem__(self, item):
        """Extrait une partie de la grille.
        On peut extraire un seul élément [x,y], une ligne [x1:x2,y],
        une colonne [x,y1:y2], un rectangle[x1:x2,y1:y2] ou toute la grille [...]
        Renvoie un array bidimensionnel numpy
        """
        return self.array[self.translate_coordinates(item)]

    def __setitem__(self, item, value):
        """Définie un partie de la grille. Les éléments doivent être
        un seul entier ou des entiers dans un array numpy.
        Un 0 correspond à une cellule morte, un 1 à une cellule vivante.
        Il faut utiliser les mêmes notation que pour __getitem__
        """
        self.array[self.translate_coordinates(item)] = value
