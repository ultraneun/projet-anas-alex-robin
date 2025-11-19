import pyxel
class module:
    def __init__(self):
        self.explosions_liste = []
        
    def explosions_creation(self, x, y):
        """explosions aux points de collision entre deux objets"""
        self.explosions_liste.append([x, y, 0])


    def explosions_animation(self):
        """animation des explosions"""
        for explosion in self.explosions_liste:
            explosion[2] +=1
            if explosion[2] == 12:
                self.explosions_liste.remove(explosion)

    # --- Logique du joueur déplacée depuis main.py ---
    def deplacement(self, jeu):
        """Gère la lecture des touches pour déplacer le vaisseau."""
        if pyxel.btn(pyxel.KEY_D) and jeu.vaisseau_x < 120:
            jeu.vaisseau_x += 2
        if pyxel.btn(pyxel.KEY_Q) and jeu.vaisseau_x > 0:
            jeu.vaisseau_x -= 2
        if pyxel.btn(pyxel.KEY_S) and jeu.vaisseau_y < 120:
            jeu.vaisseau_y += 2
        if pyxel.btn(pyxel.KEY_Z) and jeu.vaisseau_y > 0:
            jeu.vaisseau_y -= 2

    def vaisseau_suppression(self, jeu):
        """Gère les collisions entre le vaisseau et ennemis / tirs ennemis.

        Cette méthode remplace l'ancienne fonction présente dans `main.py`.
        Elle utilise `jeu.adversaire`, `jeu.tir`, `jeu.gestion_score` et
        `self.explosions_creation` pour appliquer les effets.
        """
        # Collisions avec les ennemis rapides
        for ennemi in jeu.adversaire.ennemis_rapides_liste[:]:
            if (ennemi[0] <= jeu.vaisseau_x + 8 and ennemi[1] <= jeu.vaisseau_y + 8 and
                ennemi[0] + 8 >= jeu.vaisseau_x and ennemi[1] + 8 >= jeu.vaisseau_y):
                try:
                    jeu.adversaire.ennemis_rapides_liste.remove(ennemi)
                except ValueError:
                    pass
                # décrémenter la vie via GestionScore
                jeu.gestion_score.retirer_vie()
                self.explosions_creation(jeu.vaisseau_x, jeu.vaisseau_y)

        # Collisions avec les tirs ennemis
        for tir in jeu.tir.tirs_ennemis_liste[:]:
            tir_x, tir_y = tir[0], tir[1]
            if (tir_x <= jeu.vaisseau_x + 8 and tir_x + 2 >= jeu.vaisseau_x and
                tir_y <= jeu.vaisseau_y + 8 and tir_y + 4 >= jeu.vaisseau_y):
                try:
                    jeu.tir.tirs_ennemis_liste.remove(tir)
                except ValueError:
                    pass
                # retirer une vie et afficher une explosion
                jeu.gestion_score.retirer_vie()
                self.explosions_creation(jeu.vaisseau_x, jeu.vaisseau_y)

    # ----- Orchestration du monde de jeu (raccourcit main.py) -----
    def scroll_world(self, jeu):
        """Gère le scrolling vertical du fond."""
        if jeu.scroll_y > 384:
            jeu.scroll_y -= 1
        else:
            jeu.scroll_y = 960

    def activer_bonus_laser(self, jeu):
        """Active le bonus laser (appelé depuis le jeu).

        Cette méthode conserve la compatibilité avec l'API précédente.
        """
        jeu.bonus_laser_actif = True
        jeu.bonus_laser_timer = jeu.bonus_laser_duree

    def update_bonus_laser(self, jeu):
        """Met à jour le timer du bonus laser."""
        if jeu.bonus_laser_actif:
            jeu.bonus_laser_timer -= 1
            if jeu.bonus_laser_timer <= 0:
                jeu.bonus_laser_actif = False

    def update_world(self, jeu):
        """Orchestre la mise à jour principale du jeu (déplacement, tirs,
        ennemis, collisions, lasers, explosions, scroll).

        Appel unique depuis `main.py` pour réduire sa taille.
        """
        # Mise à jour des paramètres d'apparition
        try:
            jeu.adversaire.mettre_a_jour_vitesse_apparition()
        except Exception:
            pass

        # Mouvements du joueur
        self.deplacement(jeu)

        # Gestion du sens de tir à lire ici
        sens = None
        if pyxel.btnr(pyxel.KEY_SPACE):
            sens = 1
        elif pyxel.btnr(pyxel.KEY_LEFT):
            sens = 0
        elif pyxel.btnr(pyxel.KEY_RIGHT):
            sens = 2

        # Tir laser via charges (touche A). Chaque tir consomme 1 charge.
        if getattr(jeu, "laser_charges", 0) > 0 and pyxel.btnr(pyxel.KEY_A) and jeu.tir.laser_peut_tirer():
            jeu.tir.laser_creation(jeu.vaisseau_x, jeu.vaisseau_y)
            jeu.laser_charges -= 1

        # Création / mises à jour des tirs/ennemis
        jeu.tir.tirs_creation(jeu.vaisseau_x, jeu.vaisseau_y, sens)
        jeu.tir.laser_update()
        jeu.tir.tirs_deplacement()
        jeu.adversaire.ennemis_creation()
        jeu.adversaire.ennemis_deplacement()
        jeu.adversaire.ennemis_tir()
        jeu.adversaire.boss_creation()
        jeu.adversaire.boss_deplacement()
        jeu.adversaire.boss_tir()
        jeu.adversaire.ennemis_suppression()

        # Collisions vaisseau
        self.vaisseau_suppression(jeu)

        # Collisions laser -> ennemis (délégué à Tir)
        try:
            jeu.tir.laser_collisions(jeu.adversaire, self, jeu.gestion_score)
        except Exception:
            pass

        # Animations d'explosions
        self.explosions_animation()

        # Scroll du fond
        self.scroll_world(jeu)

        # Mise à jour du timer du bonus laser
        self.update_bonus_laser(jeu)

class Colisions:
    def __init__(self):
        pass
    
    def reactionss_collision(self, a, b, size_a=(8,8), size_b=(8,8)):
        """Retourne True si les rectangles a et b se chevauchent.

        a et b sont des tuples/listes (x, y). size_a/size_b donnent la largeur/hauteur.
        """
        ax, ay = a[0], a[1]
        bx, by = b[0], b[1]
        aw, ah = size_a
        bw, bh = size_b
        return (ax <= bx + bw and ax + aw >= bx and ay <= by + bh and ay + ah >= by)