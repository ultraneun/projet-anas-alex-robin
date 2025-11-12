import pyxel
import random

class ennemis:
    def __init__(self, tir_instance, explosions_creation, score_obj=None):
        # type 0 = Tank (3 PV), 1 = Tireur (rebondit et tire), 2 = Rapide (double vitesse) 3=boss
        self.ennemis_liste = []
        self.ennemis_rapides_liste = []
        self.boss_liste = []
        self.tir = tir_instance
        self.explosions_creation = explosions_creation
        self.score_obj = score_obj
        self.vitesse_apparition = 16
        self.skins_ennemis = [(0, 32), (8, 40), (8, 32)]  # Coordonnées des fantomes pour les 3 types
        self.boss_apparu = False
        self.boss_vaincu = False

    def mettre_a_jour_vitesse_apparition(self):
        pass
        #if self.score_obj % 1500 == 0:  
         #  self.vitesse_apparition = max(7, 16 - (self.score_obj.score // 1500))

    def boss_creation(self):
        """Création du boss quand le score atteint 2000 points."""
        if self.score_obj is not None and not self.boss_apparu:
            try:
                if self.score_obj.score >= 2000:
                    # Boss au centre de l'écran en haut
                    # [x, y, type, pv, direction, phase_attaque]
                    self.boss_liste.append([56, 10, 3, 50, 1, 0])
                    self.boss_apparu = True
            except Exception:
                pass

    def boss_deplacement(self):
        """Déplacement du boss : zigzag horizontal en haut de l'écran."""
        nouvelle_liste_boss = []
        for x, y, boss_type, pv, direction, phase in self.boss_liste:
            # Mouvement horizontal
            x += direction * 2
            
            # Rebondit sur les bords
            if x <= 0 or x >= 104:  # 104 car le boss fait 16x16
                direction *= -1
                x = max(0, min(x, 104))
            
            # Descend légèrement de temps en temps
            if pyxel.frame_count % 120 == 0:
                y = min(y + 5, 30)
            
            nouvelle_liste_boss.append([x, y, boss_type, pv, direction, phase])
        
        self.boss_liste = nouvelle_liste_boss

    def boss_tir(self):
        """Le boss tire 3 projectiles en éventail toutes les 2 secondes."""
        if len(self.boss_liste) > 0 and pyxel.frame_count % 120 == 0:
            boss = self.boss_liste[0]
            # Tir central
            self.tir.ajouter_tir_ennemi(boss[0] + 8, boss[1] + 16)
            # Tir gauche (légèrement décalé)
            self.tir.ajouter_tir_ennemi(boss[0] + 4, boss[1] + 16)
            # Tir droite (légèrement décalé)
            self.tir.ajouter_tir_ennemi(boss[0] + 12, boss[1] + 16)

    def ennemis_creation(self):
        """Création aléatoire des 3 types d'ennemis spéciaux."""
        # Ne créé plus d'ennemis normaux si le boss est présent
        if len(self.boss_liste) > 0:
            return

        if pyxel.frame_count % self.vitesse_apparition == 0:
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
        boss_a_supprimer = set()
        tirs_a_supprimer = set()

        for i, ennemi in enumerate(self.ennemis_liste):
            for j, tir in enumerate(self.tir.tirs_liste):
                if self._detecter_collision(ennemi, tir):
                    ennemis_lents_a_supprimer.add(i)
                    tirs_a_supprimer.add(j)
                    ennemi[3] -= 1
                    if ennemi[3] <= 0:
                        self.explosions_creation(ennemi[0], ennemi[1])
                        if self.score_obj is not None:
                            try:
                                self.score_obj.ajouter_score(100)
                            except Exception:
                                pass

        for i, ennemi in enumerate(self.ennemis_rapides_liste):
            for j, tir in enumerate(self.tir.tirs_liste):
                if self._detecter_collision(ennemi, tir):
                    ennemis_rapides_a_supprimer.add(i)
                    tirs_a_supprimer.add(j)
                    ennemi[3] -= 1
                    if ennemi[3] <= 0:
                        self.explosions_creation(ennemi[0], ennemi[1])
                        if self.score_obj is not None:
                            try:
                                self.score_obj.ajouter_score(100)
                            except Exception:
                                pass

        # Collision avec le boss (16x16 pixels)
        for i, boss in enumerate(self.boss_liste):
            for j, tir in enumerate(self.tir.tirs_liste):
                if self._detecter_collision_boss(boss, tir):
                    tirs_a_supprimer.add(j)
                    boss[3] -= 1  # Enlève 1 PV
                    if boss[3] <= 0:
                        self.explosions_creation(boss[0], boss[1])
                        self.explosions_creation(boss[0] + 8, boss[1] + 8)  # Double explosion
                        boss_a_supprimer.add(i)
                        self.boss_vaincu = True
                        if self.score_obj is not None:
                            try:
                                self.score_obj.ajouter_score(5000)  # Gros bonus
                            except Exception:
                                pass

        # Mise à jour des listes
        self.ennemis_liste = [
            ennemi for idx, ennemi in enumerate(self.ennemis_liste)
            if idx not in ennemis_lents_a_supprimer or ennemi[3] > 0
        ]
        self.ennemis_rapides_liste = [
            ennemi for idx, ennemi in enumerate(self.ennemis_rapides_liste)
            if idx not in ennemis_rapides_a_supprimer or ennemi[3] > 0
        ]
        self.boss_liste = [
            boss for idx, boss in enumerate(self.boss_liste)
            if idx not in boss_a_supprimer
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

    def _detecter_collision_boss(self, boss, tir):
        """Détection de collision entre le boss (16x16) et un tir."""
        return (boss[0] <= tir[0] + 8 and
                boss[0] + 16 >= tir[0] and
                boss[1] <= tir[1] + 8 and
                boss[1] + 16 >= tir[1])
