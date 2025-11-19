# -*- coding: utf-8 -*-
import pyxel
import random
from notre_jeu import modules_base, adversaire, tir, skin, bonus_malus, Score

TRANSPARENT_COLOR = 0
BOSS_MAX_PV = 50
class Jeu:
    def __init__(self):
        pyxel.init(128, 128, title="Space Game", display_scale=7)
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
        # transmettre l'objet de score à l'instance d'ennemis pour permettre l'incrémentation
        self.adversaire = adversaire.ennemis(self.tir, self.modules_base.explosions_creation, self.gestion_score)
        self.scroll_y = 960
        self.musique_en_cours = False#musique pyxel
        
        # ========== BONUS LASER ==========
        self.bonus_laser_actif = False  # Devient True quand on ramasse le bonus
        self.bonus_laser_duree = 300  # 10 secondes à 30 FPS
        self.bonus_laser_timer = 0  # Timer du bonus
        # Charges de laser récupérées via les coeurs
        self.laser_charges = 0
        #etat du la victoire :
        self.win = False
        
        pyxel.run(self.update, self.draw)
        

    # --------------------
    # UPDATE
    # --------------------
    def update(self):
        # ÉTAT MENU
        if self.menu_skins.etat in ["menu", "skins", "skins_vaisseau", "regles", "commandes"]:
            if self.musique_en_cours:
                pyxel.stop()
                self.musique_en_cours = False
            self.menu_skins.update()
            if self.menu_skins.etat == "menu" and pyxel.btnr(pyxel.KEY_RETURN) and self.menu_skins.menu_choix == 0:
                self.reset_game()
                self.menu_skins.etat = "jeu"
            return

        # SI GAGNÉ → STOPPER LE JEU
        if self.win:
            if pyxel.btnr(pyxel.KEY_RETURN):
                self.reset_game()
                self.menu_skins.etat = "menu"
                self.win = False
            return


        # SI GAME OVER
        if self.gestion_score.vies <= 0:
            if pyxel.btnr(pyxel.KEY_RETURN):
                self.menu_skins.etat = "menu"
            return

        # Lancer la musique
        if not self.musique_en_cours:
            pyxel.playm(0, loop=True)
            self.musique_en_cours = True

        # Update du jeu
        self.update_jeu()

    # --------------------
    # DRAW
    # --------------------
    def draw(self):
        pyxel.cls(0)

        # MENUS
        if self.menu_skins.etat in ["menu", "skins", "skins_vaisseau", "regles", "commandes"]:
            self.menu_skins.draw()
            return

        # ecran you win
        if self.win:
            pyxel.cls(0)
            pyxel.text(40, 60, "YOU WIN !", 10)
            pyxel.text(22, 80, "ENTER pour retourner", 7)
            return

        # ecran game over
        if self.gestion_score.vies <= 0:
            if pyxel.btnr(pyxel.KEY_RETURN):
                self.reset_game()
                self.menu_skins.etat = "menu"
            return

        # DESSIN DU JEU
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
        self.adversaire = adversaire.ennemis(self.tir, self.modules_base.explosions_creation, self.gestion_score)
        self.scroll_y = 960
        # Réinitialise le bonus laser
        self.bonus_laser_actif = False
        self.bonus_laser_timer = 0
        # Réinitialise les charges de laser
        self.laser_charges = 0

    def deplacement(self):
        if pyxel.btn(pyxel.KEY_D) and self.vaisseau_x < 120:
            self.vaisseau_x += 2
        if pyxel.btn(pyxel.KEY_Q) and self.vaisseau_x > 0:
            self.vaisseau_x -= 2
        if pyxel.btn(pyxel.KEY_S) and self.vaisseau_y < 120:
            self.vaisseau_y += 2
        if pyxel.btn(pyxel.KEY_Z) and self.vaisseau_y > 0:
            self.vaisseau_y -= 2

    def vaisseau_suppression(self):
        # Collisions avec les ennemis rapides
        for ennemi in self.adversaire.ennemis_rapides_liste[:]:
            if (ennemi[0] <= self.vaisseau_x + 8 and ennemi[1] <= self.vaisseau_y + 8 and
                ennemi[0] + 8 >= self.vaisseau_x and ennemi[1] + 8 >= self.vaisseau_y):
                self.adversaire.ennemis_rapides_liste.remove(ennemi)
                 # décrémenter la vie via GestionScore
                self.gestion_score.retirer_vie()
                self.modules_base.explosions_creation(self.vaisseau_x, self.vaisseau_y)

        # Collisions avec les tirs ennemis
        for tir in self.tir.tirs_ennemis_liste[:]:
            # tirs ennemis : [x, y], taille approximative 2x4 (voir notre_jeu/tir.py)
            tir_x, tir_y = tir[0], tir[1]
            if (tir_x <= self.vaisseau_x + 8 and tir_x + 2 >= self.vaisseau_x and
                tir_y <= self.vaisseau_y + 8 and tir_y + 4 >= self.vaisseau_y):
                try:
                    self.tir.tirs_ennemis_liste.remove(tir)
                except ValueError:
                    pass
                # retirer une vie et afficher une explosion
                self.gestion_score.retirer_vie()
                self.modules_base.explosions_creation(self.vaisseau_x, self.vaisseau_y)

    # ========== COLLISIONS LASER-ENNEMIS ==========
    def laser_collisions(self):
        """Gère les collisions entre les lasers et les ennemis"""
        hitboxes = self.tir.laser_get_hitbox()
        
        for hitbox in hitboxes:
            hx, hy, hw, hh = hitbox
            
            # Collision avec ennemis rapides
            for ennemi in self.adversaire.ennemis_rapides_liste[:]:
                ex, ey = ennemi[0], ennemi[1]
                
                # Collision rectangulaire
                if (hx < ex + 8 and hx + hw > ex and
                    hy < ey + 8 and hy + hh > ey):
                    try:
                        self.adversaire.ennemis_rapides_liste.remove(ennemi)
                        # Ajoute des points
                        self.gestion_score.ajouter_score(100)
                        self.modules_base.explosions_creation(ex, ey)
                    except ValueError:
                        pass
            
            # Collision avec boss
            for boss in self.adversaire.boss_liste[:]:
                bx, by = boss[0], boss[1]
                
                # Boss fait 16x16
                if (hx < bx + 16 and hx + hw > bx and
                    hy < by + 16 and hy + hh > by):
                    # Dans `adversaire.boss_liste` la structure est [x,y,type,pv,direction,phase]
                    # Les PV sont en position 3.
                    boss[3] -= 2  # Le laser enlève 2 PV au boss par collision
                    if boss[3] <= 0:
                        try:
                            self.adversaire.boss_liste.remove(boss)
                            # Ajoute des points pour le boss (gros bonus)
                            if self.gestion_score is not None:
                                try:
                                    self.gestion_score.ajouter_score(5000)
                                except Exception:
                                    pass
                            # Double explosion comme côté adversaire
                            self.modules_base.explosions_creation(bx, by)
                            self.modules_base.explosions_creation(bx + 8, by + 8)
                        except ValueError:
                            pass
        
    def scroll(self):
        if self.scroll_y > 384:
            self.scroll_y -= 1
        else:
            self.scroll_y = 960

    # ========== GESTION BONUS LASER ==========
    def activer_bonus_laser(self):
        """Active le bonus laser (appelé quand le joueur ramasse le bonus)"""
        self.bonus_laser_actif = True
        self.bonus_laser_timer = self.bonus_laser_duree

    def update_bonus_laser(self):
        """Met à jour le timer du bonus laser"""
        if self.bonus_laser_actif:
            self.bonus_laser_timer -= 1
            if self.bonus_laser_timer <= 0:
                self.bonus_laser_actif = False

    def update_jeu(self):
        if self.gestion_score.score >= 35000:
            self.win = True
            return
        
        # Délègue la mise à jour du monde pour alléger `main.py`
        try:
            self.modules_base.update_world(self)
        except Exception:
            pass
        
        # mise a jour des bonus/malus
        self.bonus.update()
        # mise a jour du score (timers de bonus...)
        self.gestion_score.update()
        # collisions entre joueur et coeurs/météorites
        delta_vies, delta_charges = self.bonus.check_player_collision(self.vaisseau_x, self.vaisseau_y)
        if delta_vies != 0:
            # delta_vies peut être positif (coeur) ou négatif (météorite)
            self.gestion_score.vies += delta_vies
        if delta_charges != 0:
            # Ajouter des charges de laser (ex : 1 par coeur ramassé)
            self.laser_charges += delta_charges


    def draw_jeu(self):
        if self.gestion_score.vies > 0:
            pyxel.bltm(0, 0, 0, 192, (self.scroll_y // 4) % 128, 128, 128)
            pyxel.bltm(0, 0, 0, 0, self.scroll_y, 128, 128, 0)
            self.gestion_score.draw()
            # HUD: déléguer le dessin à skin.MenuSkins
            try:
                self.menu_skins.draw_hud(self)
            except Exception:
                pass
            
            # Affichage du vaisseau
            u, v = self.menu_skins.skins_vaisseau[self.menu_skins.skin_vaisseau]
            pyxel.blt(self.vaisseau_x, self.vaisseau_y, 0, u, v, 8, 8, 0)
        
            # Affichage des ennemis rapides
            for ennemi in self.adversaire.ennemis_rapides_liste:
                u_r, v_r = self.adversaire.skins_ennemis[ennemi[2]]
                pyxel.blt(ennemi[0], ennemi[1], 0, u_r, v_r, 8, 8, 0)
            
            # ⭐ AFFICHAGE DU BOSS ⭐
            for boss in self.adversaire.boss_liste:
                pyxel.blt(boss[0], boss[1], 0, 32, 0, 32, 16 ,0)
                # Barre de PV au-dessus du boss
                try:
                    bx, by = boss[0], boss[1]
                    pv = boss[3]
                except Exception:
                    continue
                bar_w = 32
                bar_h = 4
                bar_x = bx
                bar_y = max(0, by - 8)
                # fond (gris/noir)
                pyxel.rect(bar_x, bar_y, bar_w, bar_h, 0)
                # remplissage proportionnel
                fill_w = 0
                if BOSS_MAX_PV > 0:
                    fill_w = int(bar_w * max(0, min(pv, BOSS_MAX_PV)) / BOSS_MAX_PV)
                if fill_w > 0:
                    pyxel.rect(bar_x, bar_y, fill_w, bar_h, 10)
                # bordure
                pyxel.rectb(bar_x - 1, bar_y - 1, bar_w + 2, bar_h + 2, 7)
            
            # Affichage des tirs (joueur, ennemis ET LASERS)
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