# -*- coding: utf-8 -*-
import pyxel

class Tir:
    def __init__(self):
        # Liste des tirs du joueur : [x, y, sens]
        self.tirs_liste = []
        # Liste des tirs ennemis : [x, y]
        self.tirs_ennemis_liste = []
        
        # ========== LASER PUISSANT ==========
        # Liste des lasers actifs : [x, y, longueur_actuelle]
        self.lasers_liste = []
        # Paramètres du laser
        self.laser_largeur = 5  # Largeur du laser (nombre de lignes)
        self.laser_longueur_max = 40  # Longueur maximale du laser
        self.laser_vitesse_croissance = 5  # Vitesse d'expansion
        self.laser_vitesse_deplacement = 4  # Vitesse de descente
        self.laser_cooldown = 0  # Cooldown entre les tirs
        self.laser_cooldown_max = 45  # 1.5 secondes à 30 FPS

    def tirs_creation(self, vaisseau_x, vaisseau_y, sens=None):
        """Création d'un tir du joueur.
        Le paramètre `sens` doit être fourni par le code appelant.
        Si `sens` est None, aucun tir n'est créé.
        """
        if sens is None:
            return
        # On crée le tir légèrement au-dessus du vaisseau
        if sens == 2:
            start_x = vaisseau_x + 8
        elif sens == 0:
            start_x = vaisseau_x
        else:
            start_x = vaisseau_x 

        self.tirs_liste.append([start_x, vaisseau_y - 8, sens])

    def ajouter_tir_ennemi(self, x, y):
        """Ajoute un tir ennemi."""
        self.tirs_ennemis_liste.append([x, y])

    # ========== FONCTIONS LASER ==========
    
    def laser_peut_tirer(self):
        """Vérifie si on peut tirer un laser (cooldown terminé)"""
        return self.laser_cooldown <= 0
    
    def laser_creation(self, vaisseau_x, vaisseau_y):
        """Crée un nouveau laser depuis le vaisseau"""
        if self.laser_peut_tirer():
            # Position de départ : centre du vaisseau (8x8)
            self.lasers_liste.append([vaisseau_x + 4, vaisseau_y, 0])
            self.laser_cooldown = self.laser_cooldown_max
    
    def laser_update(self):
        """Met à jour le cooldown du laser"""
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1
    
    def lasers_deplacement(self):
        """Déplace et fait grandir les lasers"""
        nouvelle_liste = []
        for laser in self.lasers_liste:
            x, y, longueur = laser[0], laser[1], laser[2]
            
            # Fait MONTER le laser (signe - au lieu de +)
            y -= self.laser_vitesse_deplacement
            
            # Fait grandir le laser jusqu'à la longueur max
            if longueur < self.laser_longueur_max:
                longueur += self.laser_vitesse_croissance
            
            # Garde le laser s'il est encore visible (vérifie en haut de l'écran)
            if y + longueur > 0:  # Si le laser n'est pas complètement sorti en haut
                nouvelle_liste.append([x, y, longueur])
        
        self.lasers_liste = nouvelle_liste
    
    def lasers_affichage(self):
        """Affiche tous les lasers actifs"""
        for laser in self.lasers_liste:
            x, y, longueur = laser[0], laser[1], laser[2]
            
            # Dessine plusieurs lignes pour créer un laser large
            for i in range(self.laser_largeur):
                # Ligne principale (au centre)
                offset = i - self.laser_largeur // 2  # Ex: -2, -1, 0, 1, 2 pour largeur=5
                
                # Point de départ (en bas, position actuelle du laser)
                x1 = x + offset
                y1 = y
                
                # Point d'arrivée (en haut du laser - le laser MONTE)
                x2 = x + offset
                y2 = y - longueur
                
                # Couleur selon la position (centre plus brillant)
                if offset == 0:
                    couleur = 7  # Blanc (centre)
                elif abs(offset) == 1:
                    couleur = 10  # Jaune (milieu)
                else:
                    couleur = 9  # Orange (côtés)
                
                # Dessine la ligne verticale
                pyxel.line(x1, y1, x2, y2, couleur)
            
            # Ajoute un point brillant à l'extrémité (en haut maintenant)
            pyxel.circ(x, y - longueur, 2, 7)
    
    def laser_get_hitbox(self):
        """Retourne les hitbox des lasers pour les collisions"""
        hitboxes = []
        for laser in self.lasers_liste:
            x, y, longueur = laser[0], laser[1], laser[2]
            # Hitbox : [x_min, y_min, largeur, hauteur]
            # Le laser monte, donc y_min est y - longueur
            hitboxes.append([
                x - self.laser_largeur // 2,  # x_min
                y - longueur,                  # y_min (en haut du laser)
                self.laser_largeur,            # largeur
                longueur                       # hauteur
            ])
        return hitboxes

    def laser_collisions(self, adversaire, modules_base, gestion_score):
        """Gère les collisions entre les lasers et les ennemis.

        Déplacé depuis `main.py` pour centraliser la logique liée aux lasers
        dans `tir.py` où sont gérés les lasers et leurs hitboxes.
        """
        hitboxes = self.laser_get_hitbox()
        for hx, hy, hw, hh in hitboxes:
            # Collision avec ennemis rapides
            for ennemi in adversaire.ennemis_rapides_liste[:]:
                ex, ey = ennemi[0], ennemi[1]
                if (hx < ex + 8 and hx + hw > ex and hy < ey + 8 and hy + hh > ey):
                    try:
                        adversaire.ennemis_rapides_liste.remove(ennemi)
                        if gestion_score is not None:
                            try:
                                gestion_score.ajouter_score(100)
                            except Exception:
                                pass
                        modules_base.explosions_creation(ex, ey)
                    except ValueError:
                        pass

            # Collision avec boss
            for boss in adversaire.boss_liste[:]:
                bx, by = boss[0], boss[1]
                # Boss fait 16x16
                if (hx < bx + 16 and hx + hw > bx and hy < by + 16 and hy + hh > by):
                    boss[3] -= 2
                    if boss[3] <= 0:
                        try:
                            adversaire.boss_liste.remove(boss)
                            if gestion_score is not None:
                                try:
                                    gestion_score.ajouter_score(5000)
                                except Exception:
                                    pass
                            modules_base.explosions_creation(bx, by)
                            modules_base.explosions_creation(bx + 8, by + 8)
                        except ValueError:
                            pass

    # ========== FONCTIONS TIRS NORMAUX ==========

    def tirs_deplacement(self):
        """Déplacement des tirs du joueur et des ennemis, suppression hors-écran."""
        # Déplacement des tirs du joueur
        nouvelle_liste_joueur = []
        for tir in self.tirs_liste:
            if len(tir) < 3:
                tir.append(1)  # compatibilité : sens par défaut = vertical
            if tir[2] == 1:
                tir[1] -= 2  # vitesse vers le haut
                if tir[1] >= -8:
                    nouvelle_liste_joueur.append(tir)
            elif tir[2] == 0:
                tir[0] -= 2  # vitesse vers la gauche
                if tir[0] >= -8:
                    nouvelle_liste_joueur.append(tir)
            elif tir[2] == 2:
                tir[0] += 2  # vitesse vers la droite
                if tir[0] <= 128:
                    nouvelle_liste_joueur.append(tir)
            else:
                tir[1] -= 2  # comportement par défaut : monter
                if tir[1] >= -8:
                    nouvelle_liste_joueur.append(tir)
        self.tirs_liste = nouvelle_liste_joueur

        # Déplacement des tirs ennemis (vers le bas)
        nouvelle_liste_ennemis = []
        for tir in self.tirs_ennemis_liste:
            tir[1] += 2  # vitesse vers le bas
            if tir[1] <= 128:
                nouvelle_liste_ennemis.append(tir)
        self.tirs_ennemis_liste = nouvelle_liste_ennemis
        
        # Déplacement des lasers
        self.lasers_deplacement()

    def tirs_affichage(self):
        """Affichage des tirs du joueur et des ennemis."""
        # Tirs du joueur
        for tir in self.tirs_liste:
            if tir[2] == 1:
                pyxel.blt(tir[0], tir[1], 0, 8, 0, 8, 8)  # sprite tir vertical
            elif tir[2] == 0:
                pyxel.blt(tir[0], tir[1], 0, 8, 24, 8, 8)  # sprite tir horizontal
            elif tir[2] == 2:
                pyxel.blt(tir[0], tir[1], 0, 8, 24, 8, 8)
            else:
                pyxel.blt(tir[0], tir[1], 0, 8, 0, 8, 8)  # sprite par défaut

        # Tirs ennemis
        for tir in self.tirs_ennemis_liste:
            pyxel.rect(tir[0], tir[1], 2, 4, 8)  # rectangle rouge pour les tirs ennemis
        
        # Affichage des lasers
        self.lasers_affichage()