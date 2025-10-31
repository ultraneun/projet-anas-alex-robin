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

        # taille de la fenetre 128x128 pixels
        # ne pas modifier
        pyxel.init(128, 128, title="Nuit du c0de")

        # position initiale du vaisseau
        # (origine des positions : coin haut gauche)
        self.vaisseau_x = 60
        self.vaisseau_y = 60

        # vies
        self.vies = 4

        # initialisation des tirs
        self.tir = tir.Tir()

        self.modules_base = modules_base.module()

        # Initialisation des ennemis (IMPORTANT : passer les bonnes références)
        self.adversaire = adversaire.ennemis(self.tir, self.modules_base.explosions_creation)
        # initialisation des explosions

        # chargement des images
        pyxel.load("notre_jeu/images.pyxres")
        
        self.scroll_y = 960

        pyxel.run(self.update, self.draw)


    def deplacement(self):
        """déplacement avec les touches de directions"""

        if pyxel.btn(pyxel.KEY_RIGHT) and self.vaisseau_x<120:
            self.vaisseau_x += 2
        if pyxel.btn(pyxel.KEY_LEFT) and self.vaisseau_x>0:
            self.vaisseau_x += -2
        if pyxel.btn(pyxel.KEY_DOWN) and self.vaisseau_y<120:
            self.vaisseau_y += 2
        if pyxel.btn(pyxel.KEY_UP) and self.vaisseau_y>0:
            self.vaisseau_y += -2
    

    def vaisseau_suppression(self):
        """Disparition du vaisseau et d'un ennemi si contact"""
        
        # Vérification collision avec ennemis LENTS
        for ennemi in self.adversaire.ennemis_liste[:]:
            if (ennemi[0] <= self.vaisseau_x + 8 and 
                ennemi[1] <= self.vaisseau_y + 8 and 
                ennemi[0] + 8 >= self.vaisseau_x and 
                ennemi[1] + 8 >= self.vaisseau_y):
                
                self.adversaire.ennemis_liste.remove(ennemi)  # ✅ Supprime dans les LENTS
                self.vies -= 1
                self.modules_base.explosions_creation(self.vaisseau_x, self.vaisseau_y)
        
        # Vérification collision avec ennemis RAPIDES
        for ennemi in self.adversaire.ennemis_rapides_liste[:]:
            if (ennemi[0] <= self.vaisseau_x + 8 and 
                ennemi[1] <= self.vaisseau_y + 8 and 
                ennemi[0] + 8 >= self.vaisseau_x and 
                ennemi[1] + 8 >= self.vaisseau_y):
                
                self.adversaire.ennemis_rapides_liste.remove(ennemi)  # ✅ Supprime dans les RAPIDES
                self.vies -= 1
                self.modules_base.explosions_creation(self.vaisseau_x, self.vaisseau_y)



    def scroll(self):
        if self.scroll_y>384:
            self.scroll_y -= 1
        else :
            self.scroll_y =960
        

    # =====================================================
    # == UPDATE
    # =====================================================
    def update(self):
        """mise à jour des variables (30 fois par seconde)"""

        # deplacement du vaisseau
        self.deplacement()

        # Détecte quelle touche a été relâchée pour définir le sens
        # sens == 1 : tir vertical vers le haut (touche SPACE)
        # sens == 0 : tir horizontal vers la gauche (touche A)
        sens = None
        if pyxel.btnr(pyxel.KEY_SPACE):
            sens = 1
        elif pyxel.btnr(pyxel.KEY_A):
            sens = 0

        self.tir.tirs_creation(self.vaisseau_x, self.vaisseau_y, sens)

        # mise a jour des positions des tirs
        self.tir.tirs_deplacement()

        # creation des ennemis
        # Gestion des ennemis
        self.adversaire.ennemis_creation()
        self.adversaire.ennemis_deplacement()
        self.adversaire.ennemis_suppression()

        # suppression du vaisseau et ennemi si contact
        self.vaisseau_suppression()

        # evolution de l'animation des explosions
        self.modules_base.explosions_animation()
        
        self.scroll()


    # =====================================================
    # == DRAW
    # =====================================================
    def draw(self):
        """création et positionnement des objets (30 fois par seconde)"""

        # vide la fenetre
        pyxel.cls(0)
       


        # si le vaisseau possede des vies le jeu continue
        if self.vies > 0:

            pyxel.camera()
           
            pyxel.bltm(0, 0, 0, 192, (self.scroll_y // 4) % 128, 128, 128)
            pyxel.bltm(0, 0, 0, 0, self.scroll_y,  128, 128, TRANSPARENT_COLOR)
           

            # affichage des vies            
            #pyxel.text(5,5+self.scroll_y, 'VIES:'+ str(self.vies), 7)
            pyxel.text(5,5, 'VIES:'+ str(self.vies), 7)

            # vaisseau (carre 8x8)
            pyxel.blt(self.vaisseau_x, self.vaisseau_y, 0, 0, 0, 8, 8, TRANSPARENT_COLOR)

            # tirs
            self.tir.tirs_affichage()

            # ennemis
            # Ennemis lents
            for ennemi in self.adversaire.ennemis_liste:
                pyxel.blt(ennemi[0], ennemi[1], 0, 0, 8, 8, 8, TRANSPARENT_COLOR)

            # Ennemis rapides
            for ennemi in self.adversaire.ennemis_rapides_liste:
                pyxel.blt(ennemi[0], ennemi[1], 0, 0, 32, 8, 8, TRANSPARENT_COLOR)

            # explosions (cercles de plus en plus grands)
            for explosion in self.modules_base.explosions_liste:
                pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3)


        # sinon: GAME OVER
        else:
            pyxel.camera(0, self.scroll_y)
            pyxel.text(50,64+self.scroll_y, 'GAME OVER', 7)

Jeu()
