print ("robincamarche")  # Affiche "robincamarche" dans la console
# -*- coding: utf-8 -*-  # Définit l'encodage du fichier en UTF-8
"""
Created on Fri Mar 18 10:42:04 2022  # Date de création du fichier

@author: Peio  # Auteur du script
"""

# on rajoute random
import pyxel, random  # Importe la bibliothèque pyxel pour le jeu et random pour l'aléatoire

TRANSPARENT_COLOR = 0  # Couleur à utiliser pour la transparence

class Jeu:  # Définition de la classe principale du jeu
    def __init__(self):  # Constructeur de la classe Jeu

        # taille de la fenetre 128x128 pixels
        # ne pas modifier
        pyxel.init(128, 128, title="Nuit du c0de")  # Initialise la fenêtre du jeu avec une taille de 128x128 pixels

        # position initiale du vaisseau
        # (origine des positions : coin haut gauche)
        self.vaisseau_x = 60  # Position initiale en x du vaisseau
        self.vaisseau_y = 60  # Position initiale en y du vaisseau

        # vies
        self.vies = 4  # Nombre de vies du vaisseau

        # initialisation des tirs
        self.tirs_liste = []  # Liste des tirs actifs

        # initialisation des ennemis
        self.ennemis_liste = []  # Liste des ennemis normaux

        self.ennemis_rapides_liste = []  # Liste des ennemis rapides

        # initialisation des explosions
        self.explosions_liste = []  # Liste des explosions

        # chargement des images
        pyxel.load("images.pyxres")  # Charge les images du jeu à partir du fichier images.pyxres
        
        self.scroll_y = 960  # Position de défilement verticale initiale du fond

        pyxel.run(self.update, self.draw)  # Lance la boucle principale du jeu, avec update et draw


    def deplacement(self):  # Gestion du déplacement du vaisseau
        """déplacement avec les touches de directions"""

        if pyxel.btn(pyxel.KEY_RIGHT) and self.vaisseau_x<120:  # Si la touche droite est pressée et ne sort pas de l'écran
            self.vaisseau_x += 2  # Déplace le vaisseau à droite
        if pyxel.btn(pyxel.KEY_LEFT) and self.vaisseau_x>0:  # Si la touche gauche est pressée et ne sort pas de l'écran
            self.vaisseau_x += -2  # Déplace le vaisseau à gauche
        if pyxel.btn(pyxel.KEY_DOWN) and self.vaisseau_y<120:  # Si la touche bas est pressée et ne sort pas de l'écran
            self.vaisseau_y += 2  # Déplace le vaisseau vers le bas
        if pyxel.btn(pyxel.KEY_UP) and self.vaisseau_y>0:  # Si la touche haut est pressée et ne sort pas de l'écran
            self.vaisseau_y += -2  # Déplace le vaisseau vers le haut


    def tirs_creation(self):  # Création d'un tir
        """création d'un tir avec la barre d'espace"""

        if pyxel.btnr(pyxel.KEY_SPACE):  # Si la barre d'espace est relâchée
            self.tirs_liste.append([self.vaisseau_x, self.vaisseau_y-8])  # Ajoute un tir à la position du vaisseau


    def tirs_deplacement(self):  # Déplacement des tirs vers le haut
        """déplacement des tirs vers le haut et suppression quand ils sortent du cadre"""

        for tir in  self.tirs_liste:  # Pour chaque tir
            tir[1] -= 1  # Déplace le tir vers le haut
            if  tir[1]<-8:  # Si le tir sort de l'écran
                self.tirs_liste.remove(tir)  # Supprime le tir


    def ennemis_creation(self):  # Création aléatoire des ennemis
        """création aléatoire des ennemis"""

        # un ennemi par seconde
        if (pyxel.frame_count % 30 == 0):  # Toutes les 30 frames (1 seconde)
            self.ennemis_liste.append([random.randint(0, 120), 0])  # Ajoute un ennemi en haut, position x aléatoire
        if (pyxel.frame_count % 150 == 0):  # Toutes les 150 frames (5 secondes)
            self.ennemis_rapides_liste.append([random.randint(0, 120), 0,3])  # Ajoute un ennemi rapide (x, y, vitesse)


    def ennemis_deplacement(self):  # Déplacement des ennemis
        """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""              

        for ennemi in self.ennemis_liste:  # Pour chaque ennemi normal
            ennemi[1] += 1  # Descend l'ennemi
            if ennemi[1]>128:  # Si l'ennemi sort de l'écran
                self.ennemis_liste.remove(ennemi)  # Supprime l'ennemi

        for ennemi in self.ennemis_rapides_liste:  # Pour chaque ennemi rapide
            ennemi[1] += 1  # Descend l'ennemi
            
            ennemi[0] += ennemi[2]  # Déplace l'ennemi horizontalement selon sa vitesse
            
            # Inverse la direction si touche un bord
            if ennemi[0] >= 120:  # Si l'ennemi touche le bord droit
                ennemi[2] = -3  # Change de direction vers la gauche
            elif ennemi[0] <= 0:  # Si l'ennemi touche le bord gauche
                ennemi[2] = 3  # Change de direction vers la droite
            
            if ennemi[1] > 128:  # Si l'ennemi sort de l'écran
                self.ennemis_rapides_liste.remove(ennemi)  # Supprime l'ennemi


    def vaisseau_suppression(self):  # Suppression du vaisseau si collision
        """disparition du vaisseau et d'un ennemi si contact"""

        for ennemi in self.ennemis_liste:  # Pour chaque ennemi normal
            if ennemi[0] <= self.vaisseau_x+8 and ennemi[1] <= self.vaisseau_y+8 and ennemi[0]+8 >= self.vaisseau_x and ennemi[1]+8 >= self.vaisseau_y:  # Si collision
                self.ennemis_liste.remove(ennemi)  # Supprime l'ennemi
                self.vies -= 1  # Enlève une vie au joueur
                # on ajoute l'explosion
                self.explosions_creation(self.vaisseau_x, self.vaisseau_y)  # Crée une explosion à la position du vaisseau
        
        for ennemi in self.ennemis_rapides_liste:  # Pour chaque ennemi rapide
            if ennemi[0] <= self.vaisseau_x+8 and ennemi[1] <= self.vaisseau_y+8 and ennemi[0]+8 >= self.vaisseau_x and ennemi[1]+8 >= self.vaisseau_y:  # Si collision
                self.ennemis_rapides_liste.remove(ennemi)  # Supprime l'ennemi rapide
                self.vies -= 1  # Enlève une vie au joueur
                # on ajoute l'explosion
                self.explosions_creation(self.vaisseau_x, self.vaisseau_y)  # Crée une explosion à la position du vaisseau


    def ennemis_suppression(self):  # Suppression des ennemis si touchés par un tir
        """disparition d'un ennemi et d'un tir si contact"""

        for ennemi in self.ennemis_liste:  # Pour chaque ennemi normal
            for tir in self.tirs_liste:  # Pour chaque tir
                if ennemi[0] <= tir[0]+8 and ennemi[0]+8 >= tir[0] and ennemi[1]+8 >= tir[1]:  # Si collision
                    self.ennemis_liste.remove(ennemi)  # Supprime l'ennemi
                    self.tirs_liste.remove(tir)  # Supprime le tir
                    # on ajoute l'explosion
                    self.explosions_creation(ennemi[0], ennemi[1])  # Crée une explosion à la position de l'ennemi
                    
        for ennemi in self.ennemis_rapides_liste:  # Pour chaque ennemi rapide
            for tir in self.tirs_liste:  # Pour chaque tir
                if ennemi[0] <= tir[0]+8 and ennemi[0]+8 >= tir[0] and ennemi[1]+8 >= tir[1]:  # Si collision
                    self.ennemis_rapides_liste.remove(ennemi)  # Supprime l'ennemi rapide
                    self.tirs_liste.remove(tir)  # Supprime le tir
                    # on ajoute l'explosion
                    self.explosions_creation(ennemi[0], ennemi[1])  # Crée une explosion à la position de l'ennemi


    def explosions_creation(self, x, y):  # Création d'une explosion
        """explosions aux points de collision entre deux objets"""
        self.explosions_liste.append([x, y, 0])  # Ajoute une explosion à la liste (x, y, temps)


    def explosions_animation(self):  # Animation des explosions
        """animation des explosions"""
        for explosion in self.explosions_liste:  # Pour chaque explosion
            explosion[2] +=1  # Incrémente le temps de l'explosion
            if explosion[2] == 12:  # Si l'animation est terminée
                self.explosions_liste.remove(explosion)  # Supprime l'explosion

    def scroll(self):  # Gestion du défilement du fond
        if self.scroll_y>384:  # Si le fond n'est pas tout en bas
            self.scroll_y -= 1  # Fait défiler vers le haut
        else :
            self.scroll_y =960  # Remet le fond en position initiale
        

    # =====================================================
    # == UPDATE
    # =====================================================
    def update(self):  # Mise à jour de l'état du jeu (30 fois par seconde)
        """mise à jour des variables (30 fois par seconde)"""

        # deplacement du vaisseau
        self.deplacement()  # Met à jour la position du vaisseau

        # creation des tirs en fonction de la position du vaisseau
        self.tirs_creation()  # Crée des tirs si besoin

        # mise a jour des positions des tirs
        self.tirs_deplacement()  # Déplace les tirs

        # creation des ennemis
        self.ennemis_creation()  # Crée des ennemis

        # mise a jour des positions des ennemis
        self.ennemis_deplacement()  # Déplace les ennemis

        # suppression des ennemis et tirs si contact
        self.ennemis_suppression()  # Supprime les ennemis touchés par les tirs

        # suppression du vaisseau et ennemi si contact
        self.vaisseau_suppression()  # Vérifie les collisions entre le vaisseau et les ennemis

        # evolution de l'animation des explosions
        self.explosions_animation()  # Met à jour les explosions
        
        self.scroll()  # Met à jour le défilement du fond


    # =====================================================
    # == DRAW
    # =====================================================
    def draw(self):  # Affichage des objets du jeu (30 fois par seconde)
        """création et positionnement des objets (30 fois par seconde)"""

        # vide la fenetre
        pyxel.cls(0)  # Efface l'écran avec la couleur noire
       


        # si le vaisseau possede des vies le jeu continue
        if self.vies > 0:  # Si le joueur a encore des vies

            pyxel.camera()  # Réinitialise la caméra de Pyxel
           
            pyxel.bltm(0, 0, 0, 192, (self.scroll_y // 4) % 128, 128, 128)  # Affiche le fond en mode tiled map
            pyxel.bltm(0, 0, 0, 0, self.scroll_y,  128, 128, TRANSPARENT_COLOR)  # Affiche le fond avec transparence
           

            # affichage des vies            
            #pyxel.text(5,5+self.scroll_y, 'VIES:'+ str(self.vies), 7)
            pyxel.text(5,5, 'VIES:'+ str(self.vies), 7)  # Affiche le nombre de vies restantes

            # vaisseau (carre 8x8)
            pyxel.blt(self.vaisseau_x, self.vaisseau_y, 0, 0, 0, 8, 8, TRANSPARENT_COLOR)  # Affiche le vaisseau

            # tirs
            for tir in self.tirs_liste:  # Pour chaque tir
                pyxel.blt(tir[0], tir[1], 0, 8, 0, 8, 8)  # Affiche le tir

            # ennemis
            for ennemi in self.ennemis_liste:  # Pour chaque ennemi normal
                pyxel.blt(ennemi[0], ennemi[1], 0, 0, 8, 8, 8)  # Affiche l'ennemi

            for ennemi in self.ennemis_rapides_liste:  # Pour chaque ennemi rapide
                pyxel.blt(ennemi[0], ennemi[1], 0, 0, 32, 8, 8)  # Affiche l'ennemi rapide

            # explosions (cercles de plus en plus grands)
            for explosion in self.explosions_liste:  # Pour chaque explosion
                pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3)  # Affiche l'explosion


        # sinon: GAME OVER
        else:
            pyxel.camera(0, self.scroll_y)  # Place la caméra pour afficher le fond sur "Game Over"
            pyxel.text(50,64+self.scroll_y, 'GAME OVER', 7)  # Affiche le message "GAME OVER"

Jeu()  # Crée et lance le jeu
