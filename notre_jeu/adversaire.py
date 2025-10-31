import pyxel
import random

class ennemis:
    def __init__(self, tir_instance, explosions_creation_callback):
        """
        Initialisation de la classe ennemis.
        
        Args:
            tir_instance: référence à l'instance de la classe Tir
            explosions_creation_callback: fonction callback pour créer des explosions
        """
        # initialisation des listes d'ennemis
        self.ennemis_liste = []
        self.ennemis_rapides_liste = []
        
        # références nécessaires pour les collisions
        self.tir = tir_instance
        self.explosions_creation = explosions_creation_callback
        

    def ennemis_creation(self):
        """création aléatoire des ennemis"""

        # un ennemi par seconde
        if (pyxel.frame_count % 30 == 0):
            self.ennemis_liste.append([random.randint(0, 120), 0])
        if pyxel.frame_count % 150 == 0:
            # Position X, Position Y, Direction (1 = droite, -1 = gauche)
            direction = random.choice([1, -1])  # Choisit aléatoirement droite ou gauche
            self.ennemis_rapides_liste.append([random.randint(0, 120), 0, direction])

    def ennemis_deplacement(self):
        """Déplacement des ennemis vers le bas"""
        # Déplacement des ennemis lents (vitesse 1)
        self.ennemis_liste = [
            [ennemi[0], ennemi[1] + 1] 
            for ennemi in self.ennemis_liste 
            if ennemi[1] + 1 <= 128
        ]

        # Déplacement des ennemis rapides avec zigzags
        nouvelle_liste_rapides = []
        for ennemi in self.ennemis_rapides_liste:
            x = ennemi[0]
            y = ennemi[1]
            direction = ennemi[2]
            
            # Déplacement vertical (descente)
            y += 1
            
            # Déplacement horizontal (zigzag)
            x += direction * 3  # Vitesse horizontale de 2 pixels
            
            # Rebond sur les bords gauche et droit
            if x <= 0:  # Touche le bord gauche
                x = 0
                direction = 1  # Change de direction vers la droite
            elif x >= 120:  # Touche le bord droit (128 - 8 pixels de largeur)
                x = 120
                direction = -1  # Change de direction vers la gauche
            
            # Garde l'ennemi seulement s'il est encore dans l'écran
            if y <= 128:
                nouvelle_liste_rapides.append([x, y, direction])

        self.ennemis_rapides_liste = nouvelle_liste_rapides

    def ennemis_suppression(self): 
        """Détection et suppression des collisions entre ennemis et tirs"""
        
        # Ensembles pour marquer les indices à supprimer
        ennemis_lents_a_supprimer = set()
        ennemis_rapides_a_supprimer = set()
        tirs_a_supprimer = set()

        # Vérification des collisions avec les ennemis lents
        for i, ennemi in enumerate(self.ennemis_liste):
            for j, tir in enumerate(self.tir.tirs_liste):
                # Détection de collision rectangulaire
                if (ennemi[0] <= tir[0] + 8 and 
                    ennemi[0] + 8 >= tir[0] and 
                    ennemi[1] <= tir[1] + 8 and 
                    ennemi[1] + 8 >= tir[1]):
                    
                    ennemis_lents_a_supprimer.add(i)
                    tirs_a_supprimer.add(j)
                    self.explosions_creation(ennemi[0], ennemi[1])

        # Vérification des collisions avec les ennemis rapides
        for i, ennemi in enumerate(self.ennemis_rapides_liste):
            for j, tir in enumerate(self.tir.tirs_liste):
                # On utilise ennemi[0] pour X et ennemi[1] pour Y
                # (ennemi[2] c'est la direction, on l'ignore ici)
                if (ennemi[0] <= tir[0] + 8 and 
                    ennemi[0] + 8 >= tir[0] and 
                    ennemi[1] <= tir[1] + 8 and 
                    ennemi[1] + 8 >= tir[1]):
                    
                    ennemis_rapides_a_supprimer.add(i)
                    tirs_a_supprimer.add(j)
                    self.explosions_creation(ennemi[0], ennemi[1])
                    # Debug : affiche un message dans la console

        # Reconstruire les listes en excluant les éléments marqués
        if tirs_a_supprimer:
            self.tir.tirs_liste = [
                tir for idx, tir in enumerate(self.tir.tirs_liste) 
                if idx not in tirs_a_supprimer
            ]

        if ennemis_lents_a_supprimer:
            self.ennemis_liste = [
                ennemi for idx, ennemi in enumerate(self.ennemis_liste) 
                if idx not in ennemis_lents_a_supprimer
            ]

        if ennemis_rapides_a_supprimer:
            self.ennemis_rapides_liste = [
                ennemi for idx, ennemi in enumerate(self.ennemis_rapides_liste) 
                if idx not in ennemis_rapides_a_supprimer
            ]