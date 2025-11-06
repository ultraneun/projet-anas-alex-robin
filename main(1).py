
import pyxel
import random
from notre_jeu import modules_base, adversaire, tir, skin, bonus_malus, Score


class Jeu:
    def __init__(self):
        pyxel.init(128, 128, title="Space Game")
        pyxel.load("notre_jeu/images.pyxres")
        # --------------------
        # MENU & SKINS
        # --------------------
        self.menu_skins = skin.MenuSkins()
        # --------------------
        # VARIABLES JEU
        # --------------------
        self.vaisseau_x = 60
        self.vaisseau_y = 60
        # score et vies gérés par GestionScore
        self.gestion_score = Score.GestionScore()
        self.tir = tir.Tir()
        self.modules_base = modules_base.module()
        # initialisation des bonus/malus (coeurs et météorites)
        self.bonus = bonus_malus.BonusMalus(self.modules_base.explosions_creation)
        self.adversaire = adversaire.ennemis(self.tir, self.modules_base.explosions_creation)
        self.scroll_y = 960
        self.musique_en_cours = False#musique pyxel
        pyxel.run(self.update, self.draw)
        

    # --------------------
    # UPDATE
    # --------------------
    def update(self):
        if self.menu_skins.etat in ["menu", "skins", "skins_vaisseau"]:
            if self.musique_en_cours:
                pyxel.stop()
                self.musique_en_cours = False
            self.menu_skins.update()
            if self.menu_skins.etat == "menu" and pyxel.btnr(pyxel.KEY_RETURN) and self.menu_skins.menu_choix == 0:
                self.reset_game()
                self.menu_skins.etat = "jeu"
        else:
            if not self.musique_en_cours:
                pyxel.playm(0, loop=True)
                self.musique_en_cours = True
            self.update_jeu()

    # --------------------
    # DRAW
    # --------------------
    def draw(self):
        pyxel.cls(0)
        if self.menu_skins.etat in ["menu", "skins", "skins_vaisseau"]:
            self.menu_skins.draw()
        else:
            self.draw_jeu()

    # --------------------
    # FONCTIONS DU JEU
    # --------------------
    def reset_game(self):
        self.vaisseau_x = 60
        self.vaisseau_y = 60
        # réinitialiser gestion du score/vies
        self.gestion_score = Score.GestionScore()
        self.tir = tir.Tir()
        self.modules_base = modules_base.module()
        self.adversaire = adversaire.ennemis(self.tir, self.modules_base.explosions_creation)
        self.scroll_y = 960

    def deplacement(self):
        if pyxel.btn(pyxel.KEY_RIGHT) and self.vaisseau_x < 120:
            self.vaisseau_x += 2
        if pyxel.btn(pyxel.KEY_LEFT) and self.vaisseau_x > 0:
            self.vaisseau_x -= 2
        if pyxel.btn(pyxel.KEY_DOWN) and self.vaisseau_y < 120:
            self.vaisseau_y += 2
        if pyxel.btn(pyxel.KEY_UP) and self.vaisseau_y > 0:
            self.vaisseau_y -= 2

    def vaisseau_suppression(self):
    # Collisions avec les ennemis lents
        for ennemi in self.adversaire.ennemis_rapides_liste[:]:
            if (ennemi[0] <= self.vaisseau_x + 8 and ennemi[1] <= self.vaisseau_y + 8 and
                ennemi[0] + 8 >= self.vaisseau_x and ennemi[1] + 8 >= self.vaisseau_y):
                self.adversaire.ennemis_rapides_liste.remove(ennemi)
                # décrémenter la vie via GestionScore
                self.gestion_score.retirer_vie()
                self.modules_base.explosions_creation(self.vaisseau_x, self.vaisseau_y)

        
    def scroll(self):
        if self.scroll_y > 384:
            self.scroll_y -= 1
        else:
            self.scroll_y = 960

    def update_jeu(self):
        if self.gestion_score.vies <= 0:
            if pyxel.btnr(pyxel.KEY_RETURN):
                self.reset_game()
                self.menu_skins.etat = "menu"
            return
        self.deplacement()
        sens = None
        if pyxel.btnr(pyxel.KEY_SPACE):
            sens = 1
        elif pyxel.btnr(pyxel.KEY_A):
            sens = 0
        self.tir.tirs_creation(self.vaisseau_x, self.vaisseau_y, sens)
        self.tir.tirs_deplacement()
        self.adversaire.ennemis_creation()
        self.adversaire.ennemis_deplacement()
        self.adversaire.ennemis_tir()  
        self.adversaire.ennemis_suppression()
        self.vaisseau_suppression()  
        self.modules_base.explosions_animation()
        self.scroll()
        # mise a jour des bonus/malus
        self.bonus.update()
        # mise a jour du score (timers de bonus...)
        self.gestion_score.update()
        # collisions entre joueur et coeurs/météorites
        delta = self.bonus.check_player_collision(self.vaisseau_x, self.vaisseau_y)
        if delta != 0:
            # delta peut être positif (coeur) ou négatif (météorite)
            self.gestion_score.vies += delta
            # s'assurer que le score/etat du bonus est mis à jour si nécessaire


    def draw_jeu(self):
        if self.gestion_score.vies > 0:
            pyxel.bltm(0, 0, 0, 192, (self.scroll_y // 4) % 128, 128, 128)
            pyxel.bltm(0, 0, 0, 0, self.scroll_y, 128, 128, 0)
            self.gestion_score.draw()
            # Affichage du vaisseau
            u, v = self.menu_skins.skins_vaisseau[self.menu_skins.skin_vaisseau]
            pyxel.blt(self.vaisseau_x, self.vaisseau_y, 0, u, v, 8, 8, 0)
           
            # Affichage des ennemis rapides
            for ennemi in self.adversaire.ennemis_rapides_liste:
                u_r, v_r = self.adversaire.skins_ennemis[ennemi[2]]
                pyxel.blt(ennemi[0], ennemi[1], 0, u_r, v_r, 8, 8, 0)
            # Affichage des tirs (joueur et ennemis)
            self.tir.tirs_affichage()
            # affichage des coeurs et météorites
            self.bonus.draw()
            # Affichage des explosions
            for explosion in self.modules_base.explosions_liste:
                pyxel.circb(explosion[0] + 4, explosion[1] + 4, 2 * (explosion[2] // 4), 8 + explosion[2] % 3)
        else:
            pyxel.text(50, 64, "GAME OVER", 7)
            pyxel.text(30, 80, "ENTREE POUR MENU", 6)


Jeu()
