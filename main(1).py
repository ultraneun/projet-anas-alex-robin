# -*- coding: utf-8 -*-
"""
fait le 30 octobre 2025

@author: anas, alex, robin
"""

# on rajoute random
import pyxel, random
from notre_jeu import modules_base
from notre_jeu import adversaire
from notre_jeu import tir
TRANSPARENT_COLOR = 0

class Jeu:
    def __init__(self):
        pyxel.init(128, 128, title="Space Game")
        pyxel.load("notre_jeu/images.pyxres")

        # -----------------------
        #  ÉTAT DU JEU
        # -----------------------
        self.etat = "menu"            # menu, jeu, skins, skins_vaisseau, skins_ennemi, skins_bonus
        self.menu_choix = 0
        self.skins_menu_choix = 0

        # -----------------------
        #  SKINS DISPONIBLES
        # -----------------------
        self.skin_vaisseau = 0
        self.skin_ennemis = 0
        self.skin_ennemis_rapides = 0
        self.skin_bonus = 0

        # Coordonnées des skins dans la spritesheet
        self.skins_vaisseau = [(0,0), (0,40), (0,0)]
        self.skins_ennemis = [(0,8), (8,40), (8,32)]
        self.skins_bonus = [(8,16), (16,24), (16,16)]
        self.skins_ennemis_rapides = [(0,32), (8,24), (16,24)] 
        # -----------------------
        #  VARIABLES DU JEU
        # -----------------------
        self.vaisseau_x = 60
        self.vaisseau_y = 60
        self.vies = 4
        self.tir = tir.Tir()
        self.modules_base = modules_base.module()
        self.adversaire = adversaire.ennemis(self.tir, self.modules_base.explosions_creation)
        self.scroll_y = 960

        pyxel.run(self.update, self.draw)

    # =====================================================
    # == UPDATE
    # =====================================================
    def update(self):
        if self.etat == "menu":
            self.update_menu()
        elif self.etat == "jeu":
            self.update_jeu()
        elif self.etat == "skins":
            self.update_skins()
        elif self.etat.startswith("skins_"):
            self.update_sousmenu_skins()

    # =====================================================
    # == MENU PRINCIPAL
    # =====================================================
    def update_menu(self):
        if pyxel.btnr(pyxel.KEY_DOWN):
            self.menu_choix = (self.menu_choix + 1) % 3
        if pyxel.btnr(pyxel.KEY_UP):
            self.menu_choix = (self.menu_choix - 1) % 3

        if pyxel.btnr(pyxel.KEY_RETURN):
            if self.menu_choix == 0:
                self.reset_game()
                self.etat = "jeu"
            elif self.menu_choix == 1:
                self.skins_menu_choix = 0
                self.etat = "skins"
            elif self.menu_choix == 2:
                pyxel.quit()

    # =====================================================
    # == MENU SKINS (CHOIX DE LA CATÉGORIE)
    # =====================================================
    def update_skins(self):
        if pyxel.btnr(pyxel.KEY_DOWN):
            self.skins_menu_choix = (self.skins_menu_choix + 1) % 5  # au lieu de 4
        if pyxel.btnr(pyxel.KEY_UP):
            self.skins_menu_choix = (self.skins_menu_choix - 1) % 5

        if pyxel.btnr(pyxel.KEY_RETURN):
            if self.skins_menu_choix == 0:
                self.etat = "skins_vaisseau"
            elif self.skins_menu_choix == 1:
                self.etat = "skins_ennemis"
            elif self.skins_menu_choix == 2:
                self.etat = "skins_ennemis_rapides"
            elif self.skins_menu_choix == 3:
                self.etat = "skins_bonus"
            elif self.skins_menu_choix == 4:
                self.etat = "menu"
    # =====================================================
    # == SOUS-MENUS DE SKINS (CHOIX D'UN SKIN)
    # =====================================================
    def update_sousmenu_skins(self):
        if self.etat == "skins_vaisseau":
            if pyxel.btnr(pyxel.KEY_RIGHT):
                self.skin_vaisseau = (self.skin_vaisseau + 1) % len(self.skins_vaisseau)
            if pyxel.btnr(pyxel.KEY_LEFT):
                self.skin_vaisseau = (self.skin_vaisseau - 1) % len(self.skins_vaisseau)
        elif self.etat == "skins_ennemis":
            if pyxel.btnr(pyxel.KEY_RIGHT):
                self.skin_ennemis = (self.skin_ennemis + 1) % len(self.skins_ennemis)
            if pyxel.btnr(pyxel.KEY_LEFT):
                self.skin_ennemis = (self.skin_ennemis - 1) % len(self.skins_ennemis)
        elif self.etat == "skins_ennemis_rapides":
            if pyxel.btnr(pyxel.KEY_RIGHT):
                self.skin_ennemis_rapides = (self.skin_ennemis_rapides + 1) % len(self.skins_ennemis_rapides)
            if pyxel.btnr(pyxel.KEY_LEFT):
                self.skin_ennemis_rapides = (self.skin_ennemis_rapides - 1) % len(self.skins_ennemis_rapides)
        elif self.etat == "skins_bonus":
            if pyxel.btnr(pyxel.KEY_RIGHT):
                self.skin_bonus = (self.skin_bonus + 1) % len(self.skins_bonus)
            if pyxel.btnr(pyxel.KEY_LEFT):
                self.skin_bonus = (self.skin_bonus - 1) % len(self.skins_bonus)

        # Retour avec ENTER
        if pyxel.btnr(pyxel.KEY_RETURN):
            self.etat = "skins"

    # =====================================================
    # == UPDATE DU JEU
    # =====================================================
    def update_jeu(self):
        if self.vies <= 0:
            if pyxel.btnr(pyxel.KEY_RETURN):
                self.etat = "menu"
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
        self.adversaire.ennemis_suppression()
        self.vaisseau_suppression()
        self.modules_base.explosions_animation()
        self.scroll()

    # =====================================================
    # == DESSIN
    # =====================================================
    def draw(self):
        pyxel.cls(0)
        if self.etat == "menu":
            self.draw_menu()
        elif self.etat == "skins":
            self.draw_skins()
        elif self.etat.startswith("skins_"):
            self.draw_sousmenu_skins()
        elif self.etat == "jeu":
            self.draw_jeu()

    # -------------------------
    #  ÉCRAN DU MENU PRINCIPAL
    # -------------------------
    def draw_menu(self):
        pyxel.text(40, 30, "SPACE GAME", 10)
        options = ["JOUER", "CHANGER DE SKIN", "QUITTER"]
        for i, txt in enumerate(options):
            color = 7 if i == self.menu_choix else 5
            pyxel.text(40, 60 + i * 12, txt, color)

    # -------------------------
    #  ÉCRAN DE CHOIX DE CATÉGORIE DE SKIN
    # -------------------------
    def draw_skins(self):
        pyxel.text(30, 20, "CHOISIR CATEGORIE", 10)
        options = ["VAISSEAU","ENNEMIS", "ENNEMIS RAPIDES", "BONUS", "RETOUR"]
        for i, txt in enumerate(options):
            color = 7 if i == self.skins_menu_choix else 5
            pyxel.text(40, 50 + i * 12, txt, color)

    # -------------------------
    #  ÉCRAN DE CHOIX D’UN SKIN
    # -------------------------
    def draw_sousmenu_skins(self):
        if self.etat == "skins_vaisseau":
            liste = self.skins_vaisseau
            selection = self.skin_vaisseau
            titre = "SKIN VAISSEAU"
        elif self.etat == "skins_ennemis":
            liste = self.skins_ennemis
            selection = self.skin_ennemis
            titre = "ENNEMIS"

        elif self.etat == "skins_ennemis_rapides":
            liste = self.skins_ennemis_rapides
            selection = self.skin_ennemis_rapides
            titre = "ENNEMIS RAPIDES"
        else:
            liste = self.skins_bonus
            selection = self.skin_bonus
            titre = "SKIN BONUS"

        pyxel.text(35, 20, titre, 10)
        for i, (u,v) in enumerate(liste):
            x = 25 + i * 30
            y = 60
            pyxel.blt(x, y, 0, u, v, 8, 8, TRANSPARENT_COLOR)
            if i == selection:
                pyxel.rectb(x - 2, y - 2, 12, 12, 7)
        pyxel.text(20, 110, "ENTER = RETOUR", 5)

    # -------------------------
    #  ÉCRAN DU JEU
    # -------------------------
    def draw_jeu(self):
        if self.vies > 0:
            pyxel.bltm(0, 0, 0, 192, (self.scroll_y // 4) % 128, 128, 128)
            pyxel.bltm(0, 0, 0, 0, self.scroll_y, 128, 128, TRANSPARENT_COLOR)
            pyxel.text(5,5, 'VIES:'+ str(self.vies), 7)

            # vaisseau
            u, v = self.skins_vaisseau[self.skin_vaisseau]
            pyxel.blt(self.vaisseau_x, self.vaisseau_y, 0, u, v, 8, 8, TRANSPARENT_COLOR)

            # ennemis
            u_e, v_e = self.skins_ennemis[self.skin_ennemis]
            for ennemis in self.adversaire.ennemis_liste:
                pyxel.blt(ennemis[0], ennemis[1], 0, u_e, v_e, 8, 8, TRANSPARENT_COLOR)

            # ennemis rapides 
            u_r, v_r = self.skins_ennemis_rapides[self.skin_ennemis_rapides]
            for ennemis in self.adversaire.ennemis_rapides_liste:
                pyxel.blt(ennemis[0], ennemis[1], 0, u_r, v_r, 8, 8, TRANSPARENT_COLOR)

            

            self.tir.tirs_affichage()
            for explosion in self.modules_base.explosions_liste:
                pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3)
        else:
            pyxel.text(50,64,"GAME OVER",7)
            pyxel.text(30,80,"ENTREE POUR MENU",6)

    # =====================================================
    # == OUTILS DU JEU
    # =====================================================
    def reset_game(self):
        self.vaisseau_x = 60
        self.vaisseau_y = 60
        self.vies = 4
        self.tir = tir.Tir()
        self.modules_base = modules_base.module()
        self.adversaire = adversaire.ennemis(self.tir, self.modules_base.explosions_creation)

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
        for ennemi in self.adversaire.ennemis_liste[:]:
            if (ennemi[0] <= self.vaisseau_x + 8 and ennemi[1] <= self.vaisseau_y + 8 and
                ennemi[0] + 8 >= self.vaisseau_x and ennemi[1] + 8 >= self.vaisseau_y):
                self.adversaire.ennemis_liste.remove(ennemi)
                self.vies -= 1
                self.modules_base.explosions_creation(self.vaisseau_x, self.vaisseau_y)
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


Jeu()