# -*- coding: utf-8 -*-
import pyxel
import random
from notre_jeu import modules_base, adversaire, tir, skin

TRANSPARENT_COLOR = 0

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
        self.vies = 3
        self.tir = tir.Tir()
        self.modules_base = modules_base.module()
        self.adversaire = adversaire.ennemis(self.tir, self.modules_base.explosions_creation)
        self.scroll_y = 960
        pyxel.run(self.update, self.draw)

    # --------------------
    # UPDATE
    # --------------------
    def update(self):
        if self.menu_skins.etat in ["menu", "skins", "skins_vaisseau"]:
            self.menu_skins.update()
            if self.menu_skins.etat == "menu" and pyxel.btnr(pyxel.KEY_RETURN) and self.menu_skins.menu_choix == 0:
                self.reset_game()
                self.menu_skins.etat = "jeu"
        else:
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
        self.vies = 3
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
        

    # Collisions avec les ennemis rapides
        for ennemi in self.adversaire.ennemis_rapides_liste[:]:
            if (ennemi[0] <= self.vaisseau_x + 8 and ennemi[1] <= self.vaisseau_y + 8 and
                ennemi[0] + 8 >= self.vaisseau_x and ennemi[1] + 8 >= self.vaisseau_y):
                self.adversaire.ennemis_rapides_liste.remove(ennemi)
                self.vies -= 1
                self.modules_base.explosions_creation(self.vaisseau_x, self.vaisseau_y)

        
    def scroll(self):
        if self.scroll_y > 384:
            self.scroll_y -= 1
        else:
            self.scroll_y = 960

    def update_jeu(self):
        if self.vies <= 0:
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


    def draw_jeu(self):
        if self.vies > 0:
            pyxel.bltm(0, 0, 0, 192, (self.scroll_y // 4) % 128, 128, 128)
            pyxel.bltm(0, 0, 0, 0, self.scroll_y, 128, 128, 0)
            pyxel.text(5, 5, 'VIES:' + str(self.vies), 7)
            # Affichage du vaisseau
            u, v = self.menu_skins.skins_vaisseau[self.menu_skins.skin_vaisseau]
            pyxel.blt(self.vaisseau_x, self.vaisseau_y, 0, u, v, 8, 8, 0)
            # Affichage des ennemis lents
           
            # Affichage des ennemis rapides
            for ennemi in self.adversaire.ennemis_rapides_liste:
                u_r, v_r = self.adversaire.skins_ennemis[ennemi[2]]
                pyxel.blt(ennemi[0], ennemi[1], 0, u_r, v_r, 8, 8, 0)
            # Affichage des tirs (joueur et ennemis)
            self.tir.tirs_affichage()
            # Affichage des explosions
            for explosion in self.modules_base.explosions_liste:
                pyxel.circb(explosion[0] + 4, explosion[1] + 4, 2 * (explosion[2] // 4), 8 + explosion[2] % 3)
        else:
            pyxel.text(50, 64, "GAME OVER", 7)
            pyxel.text(30, 80, "ENTREE POUR MENU", 6)


Jeu()
