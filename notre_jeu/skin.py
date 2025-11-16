# -*- coding: utf-8 -*-
"""
Module menu et skins
"""
import pyxel

TRANSPARENT_COLOR = 0

class MenuSkins:
    def __init__(self):
        # État et choix
        self.etat = "menu"  # menu, regles, skins, skins_vaisseau, jeu
        self.menu_choix = 0
        self.skins_menu_choix = 0

        # Skins disponibles
        self.skin_vaisseau = 0

        # Coordonnées des skins dans la spritesheet
        self.skins_vaisseau = [(0,0), (0,40), (16,16)]

    # =====================================================
    # UPDATE
    # =====================================================
    def update(self):
        if self.etat == "menu":
            self.update_menu()
        elif self.etat == "regles":
            self.update_regles()
        elif self.etat == "skins":
            self.update_skins()
        elif self.etat.startswith("skins_"):
            self.update_sousmenu_skins()

    # -------------------------
    # MENU PRINCIPAL
    # -------------------------
    def update_menu(self):
        # nombre d'options = 4 (JOUER, REGLES, CHANGER DE SKIN, QUITTER)
        if pyxel.btnr(pyxel.KEY_DOWN):
            self.menu_choix = (self.menu_choix + 1) % 4
        if pyxel.btnr(pyxel.KEY_UP):
            self.menu_choix = (self.menu_choix - 1) % 4

        # Validation
        if pyxel.btnr(pyxel.KEY_RETURN):
            if self.menu_choix == 0:
                self.etat = "jeu"        # Commencer le jeu
            elif self.menu_choix == 1:
                self.etat = "regles"
            elif self.menu_choix == 2:
                self.skins_menu_choix = 0
                self.etat = "skins"      # Aller dans le menu skins
            elif self.menu_choix == 3:
                pyxel.quit()             # Quitter le jeu

    # -------------------------
    # MENU SKINS (choix catégorie)
    # -------------------------
    def update_skins(self):
        # options = ["VAISSEAU","RETOUR"] -> 2 éléments
        if pyxel.btnr(pyxel.KEY_DOWN):
            self.skins_menu_choix = (self.skins_menu_choix + 1) % 2
        if pyxel.btnr(pyxel.KEY_UP):
            self.skins_menu_choix = (self.skins_menu_choix - 1) % 2

        # Validation
        if pyxel.btnr(pyxel.KEY_RETURN):
            if self.skins_menu_choix == 0:
                self.etat = "skins_vaisseau"
            elif self.skins_menu_choix == 1:
                self.etat = "menu"  # Retour au menu principal

    # -------------------------
    # SOUS-MENU SKINS (choix d’un skin)
    # -------------------------
    def update_sousmenu_skins(self):
        if self.etat == "skins_vaisseau":
            if pyxel.btnr(pyxel.KEY_RIGHT):
                self.skin_vaisseau = (self.skin_vaisseau + 1) % len(self.skins_vaisseau)
            if pyxel.btnr(pyxel.KEY_LEFT):
                self.skin_vaisseau = (self.skin_vaisseau - 1) % len(self.skins_vaisseau)

        # Retour avec ENTER
        if pyxel.btnr(pyxel.KEY_RETURN):
            self.etat = "skins"

    # -------------------------
    # REGLES
    # -------------------------
    def update_regles(self):
        # Retour au menu si ENTER ou ESC
        if pyxel.btnr(pyxel.KEY_RETURN) or pyxel.btnr(pyxel.KEY_ESCAPE):
            self.etat = "menu"

    # =====================================================
    # DRAW
    # =====================================================
    def draw(self):
        if self.etat == "menu":
            self.draw_menu()
        elif self.etat == "regles":
            self.draw_regles()
        elif self.etat == "skins":
            self.draw_skins()
        elif self.etat.startswith("skins_"):
            self.draw_sousmenu_skins()

    def draw_menu(self):
        pyxel.cls(0)
        pyxel.text(40, 30, "SPACE GAME", 10)
        options = ["JOUER","REGLES DU JEU","CHANGER DE SKIN", "QUITTER"]
        for i, txt in enumerate(options):
            color = 7 if i == self.menu_choix else 5
            pyxel.text(40, 60 + i*12, txt, color)

    def draw_skins(self):
        pyxel.cls(0)
        pyxel.text(30, 20, "CHOISIR CATEGORIE", 10)
        options = ["VAISSEAU","RETOUR"]
        for i, txt in enumerate(options):
            color = 7 if i == self.skins_menu_choix else 5
            pyxel.text(40, 50 + i*12, txt, color)

    def draw_sousmenu_skins(self):
        pyxel.cls(0)
        if self.etat == "skins_vaisseau":
            liste = self.skins_vaisseau
            selection = self.skin_vaisseau
            titre = "SKIN VAISSEAU"
        else:
            liste = []
            selection = 0
            titre = ""

        pyxel.text(35, 20, titre, 10)
        for i, (u,v) in enumerate(liste):
            x = 25 + i*30
            y = 60
            pyxel.blt(x, y, 0, u, v, 8, 8, TRANSPARENT_COLOR)
            if i == selection:
                pyxel.rectb(x-2, y-2, 12, 12, 7)
        pyxel.text(20, 110, "ENTER = RETOUR", 5)

    def draw_regles(self):
        pyxel.cls(0)
        pyxel.text(10, 10, "REGLES DU JEU", 10)

        texte = [
    "- Evite les asteroides",
    "- 3 types d'ennemis",
    "- Violets (tuer en 3 balles)",
    "- Rouges (normaux)",
    "- Bleus (rebond et tirent)",
    "- Bouge avec les FLECHES",
    "- Tire avec ESPACE",
    "- Survis le plus longtemps",
    "- Score pour gagner : 30000",
    "- Enter pour MENU",

]


        y = 30
        for ligne in texte:
            pyxel.text(10, y, ligne, 7)
            y +=8
