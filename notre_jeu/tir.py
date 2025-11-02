# -*- coding: utf-8 -*-
import pyxel

class Tir:
    def __init__(self):
        # Liste des tirs du joueur : [x, y, sens]
        self.tirs_liste = []
        # Liste des tirs ennemis : [x, y]
        self.tirs_ennemis_liste = []

    def tirs_creation(self, vaisseau_x, vaisseau_y, sens=None):
        """Création d'un tir du joueur.
        Le paramètre `sens` doit être fourni par le code appelant.
        Si `sens` est None, aucun tir n'est créé.
        """
        if sens is None:
            return
        # On crée le tir légèrement au-dessus du vaisseau
        self.tirs_liste.append([vaisseau_x, vaisseau_y - 8, sens])

    def ajouter_tir_ennemi(self, x, y):
        """Ajoute un tir ennemi."""
        self.tirs_ennemis_liste.append([x, y])


    def tirs_deplacement(self):
        """Déplacement des tirs du joueur et des ennemis, suppression hors-écran."""
        # Déplacement des tirs du joueur
        nouvelle_liste_joueur = []
        for tir in self.tirs_liste:
            if len(tir) < 3:
                tir.append(1)  # compatibilité : sens par défaut = vertical
            if tir[2] == 1:
                tir[1] -= 2  # vitesse vers le haut
                if tir[1] >= -8:
                    nouvelle_liste_joueur.append(tir)
            elif tir[2] == 0:
                tir[0] -= 2  # vitesse vers la gauche
                if tir[0] >= -8:
                    nouvelle_liste_joueur.append(tir)
            else:
                tir[1] -= 2  # comportement par défaut : monter
                if tir[1] >= -8:
                    nouvelle_liste_joueur.append(tir)
        self.tirs_liste = nouvelle_liste_joueur

        # Déplacement des tirs ennemis (vers le bas)
        nouvelle_liste_ennemis = []
        for tir in self.tirs_ennemis_liste:
            tir[1] += 2  # vitesse vers le bas
            if tir[1] <= 128:
                nouvelle_liste_ennemis.append(tir)
        self.tirs_ennemis_liste = nouvelle_liste_ennemis

    def tirs_affichage(self):
        """Affichage des tirs du joueur et des ennemis."""
        # Tirs du joueur
        for tir in self.tirs_liste:
            if tir[2] == 1:
                pyxel.blt(tir[0], tir[1], 0, 8, 0, 8, 8)  # sprite tir vertical
            elif tir[2] == 0:
                pyxel.blt(tir[0], tir[1], 0, 8, 24, 8, 8)  # sprite tir horizontal
            else:
                pyxel.blt(tir[0], tir[1], 0, 8, 0, 8, 8)  # sprite par défaut

        # Tirs ennemis (couleur différente ou sprite différent)
        for tir in self.tirs_ennemis_liste:
            pyxel.rect(tir[0], tir[1], 2, 4, 8)  # rectangle rouge pour les tirs ennemis
