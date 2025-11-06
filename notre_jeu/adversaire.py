import pyxel
import random
from notre_jeu import Score

class ennemis:
    def __init__(self, tir_instance, explosions_creation_callback):
        # type 0 = Tank (3 PV), 1 = Tireur (rebondit et tire), 2 = Rapide (double vitesse)
        self.ennemis_liste = []
        self.ennemis_rapides_liste = []
        self.tir = tir_instance
        self.explosions_creation = explosions_creation_callback
        self.skins_ennemis = [(0, 8), (8, 40), (8, 32)]  # Coordonnées des sprites pour les 3 types

    def ennemis_creation(self):
        """Création aléatoire des 3 types d'ennemis spéciaux."""

        if pyxel.frame_count % 15 == 0:
            ennemi_type = random.randint(0, 2)  # 0, 1 ou 2
            pv = 3 if ennemi_type == 0 else 1
            direction = random.choice([1, -1])
            self.ennemis_rapides_liste.append([random.randint(0, 120), 0, ennemi_type, pv, direction])

    def ennemis_deplacement(self):
        """Déplacement des ennemis selon leur type."""
        # Déplacement des ennemis lents
        self.ennemis_liste = [
            [x, y + 1, ennemi_type, pv, direction]
            for x, y, ennemi_type, pv, direction in self.ennemis_liste
            if y + 1 <= 128
        ]

        # Déplacement des ennemis rapides
        nouvelle_liste_rapides = []
        for x, y, ennemi_type, pv, direction in self.ennemis_rapides_liste:
            y += 1
            if ennemi_type == 2:  # Rapide : double vitesse
                y += 1
            if ennemi_type == 1:  # Tireur : rebondit sur les murs
                x += direction * 2
                if x <= 0 or x >= 120:
                    direction *= -1
                    x = max(0, min(x, 120))
            if y <= 128:
                nouvelle_liste_rapides.append([x, y, ennemi_type, pv, direction])
        self.ennemis_rapides_liste = nouvelle_liste_rapides

    def ennemis_tir(self):
        """Gestion des tirs des ennemis de type 'Tireur' (un tir par seconde max)."""
        if pyxel.frame_count % 60 == 0:  # Limite la fréquence des tirs
            for ennemi in self.ennemis_rapides_liste:
                if ennemi[2] == 1:  # Si c'est un "Tireur"
                    self.tir.ajouter_tir_ennemi(ennemi[0] + 4, ennemi[1] + 8)

    def ennemis_suppression(self):
        """Suppression des ennemis touchés par les tirs du joueur."""
        ennemis_lents_a_supprimer = set()
        ennemis_rapides_a_supprimer = set()
        tirs_a_supprimer = set()

        for i, ennemi in enumerate(self.ennemis_liste):
            for j, tir in enumerate(self.tir.tirs_liste):
                if self._detecter_collision(ennemi, tir):
                    ennemis_lents_a_supprimer.add(i)
                    tirs_a_supprimer.add(j)
                    ennemi[3] -= 1
                    if ennemi[3] <= 0:
                        self.explosions_creation(ennemi[0], ennemi[1])

        for i, ennemi in enumerate(self.ennemis_rapides_liste):
            for j, tir in enumerate(self.tir.tirs_liste):
                if self._detecter_collision(ennemi, tir):
                    ennemis_rapides_a_supprimer.add(i)
                    tirs_a_supprimer.add(j)
                    ennemi[3] -= 1
                    if ennemi[3] <= 0:
                        self.explosions_creation(ennemi[0], ennemi[1])

        # Mise à jour des listes
        self.ennemis_liste = [
            ennemi for idx, ennemi in enumerate(self.ennemis_liste)
            if idx not in ennemis_lents_a_supprimer or ennemi[3] > 0
        ]
        self.ennemis_rapides_liste = [
            ennemi for idx, ennemi in enumerate(self.ennemis_rapides_liste)
            if idx not in ennemis_rapides_a_supprimer or ennemi[3] > 0
        ]
        self.tir.tirs_liste = [
            tir for idx, tir in enumerate(self.tir.tirs_liste)
            if idx not in tirs_a_supprimer
        ]

    def _detecter_collision(self, ennemi, tir):
        """Détection de collision entre un ennemi et un tir."""
        return (ennemi[0] <= tir[0] + 8 and
                ennemi[0] + 8 >= tir[0] and
                ennemi[1] <= tir[1] + 8 and
                ennemi[1] + 8 >= tir[1])
