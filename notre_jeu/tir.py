# -*- coding: utf-8 -*-
import pyxel


class Tir:
    def __init__(self):
        # La liste qui contient tous les tirs
        # Chaque tir est stocké [x, y, sens]
        # sens == 1 -> déplacement sur l'axe y (vers le haut)
        # sens == 0 -> déplacement sur l'axe x (vers la gauche)
        self.tirs_liste = []

    def tirs_creation(self, vaisseau_x, vaisseau_y, sens=None):
        """création d'un tir.

        Le paramètre `sens` doit être fourni par le code appelant (par ex. `main`).
        Si `sens` est None, aucun tir n'est créé.
        Le tir est stocké sous la forme [x, y, sens].
        """
        if sens is None:
            return
        # On crée le tir légèrement au-dessus du vaisseau
        self.tirs_liste.append([vaisseau_x, vaisseau_y - 8, sens])

    def tirs_deplacement(self):
        """déplacement des tirs selon leur sens et suppression hors-écran.

        On reconstruit la liste pour éviter de supprimer pendant l'itération.
        """
        nouvelle_liste = []
        for tir in self.tirs_liste:
            # tir = [x, y, sens]
            if len(tir) < 3:
                # compatibilité : si ancien format, on suppose vertical
                tir.append(1)

            if tir[2] == 1:
                # déplacement vertical vers le haut
                tir[1] -= 1
                # on garde le tir tant qu'il n'est pas trop haut
                if tir[1] >= -8:
                    nouvelle_liste.append(tir)
            elif tir[2] == 0:
                # déplacement horizontal vers la gauche
                tir[0] += 1
                if tir[0] >= -8:
                    nouvelle_liste.append(tir)
            else:
                # comportement par défaut : monter
                tir[1] -= 1
                if tir[1] >= -8:
                    nouvelle_liste.append(tir)

        self.tirs_liste = nouvelle_liste

    def tirs_affichage(self):
        """affichage des tirs"""
        for tir in self.tirs_liste:
            # tir[2] contient le sens : 1 = vertical, 0 = horizontal
            if tir[2] == 1:
                # Tir vertical (vers le haut)
                pyxel.blt(tir[0], tir[1], 0, 8, 0, 8, 8)
            elif tir[2] == 0:
                # Tir horizontal (vers la gauche)
                pyxel.blt(tir[0], tir[1], 0, 8, 24, 8, 8)