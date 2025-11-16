import pyxel
import math

class Laser:
    def __init__(self, x, y, direction="down"):
        self.x = x
        self.y = y
        self.direction = direction
        self.active = True
        self.longueur = 15  # Longueur de la trainée
        
        # Configure la vitesse selon la direction
        if direction == "down":
            self.dx = 0
            self.dy = 4  # Descend
        elif direction == "up":
            self.dx = 0
            self.dy = -4  # Monte
        elif direction == "right":
            self.dx = 4
            self.dy = 0
        elif direction == "left":
            self.dx = -4
            self.dy = 0
    
    def update(self):
        self.x += self.dx
        self.y += self.dy
        # Désactive si sort de l'écran
        if self.x < -5 or self.x > 165 or self.y < -5 or self.y > 125:
            self.active = False
    
    def draw(self):
        # Laser LARGE (5 pixels de largeur)
        for i in range(-2, 3):  # -2, -1, 0, 1, 2
            couleur = 7 if i == 0 else 10  # Centre blanc, bords jaunes
            
            if self.direction == "down" or self.direction == "up":
                # Laser vertical
                pyxel.line(self.x + i, self.y, 
                           self.x + i, self.y - self.dy * 3, 
                           couleur)
            else:
                # Laser horizontal
                pyxel.line(self.x, self.y + i, 
                           self.x - self.dx * 3, self.y + i, 
                           couleur)
        
        # Point brillant à la tête
        pyxel.circ(self.x, self.y, 2, 7)


class CercleExpansion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rayon = 0
        self.rayon_max = 30
        self.vitesse = 2
        self.active = True
        self.couleur = 8
    
    def update(self):
        self.rayon += self.vitesse
        if self.rayon > self.rayon_max:
            self.active = False
    
    def draw(self):
        # Cercle qui s'agrandit et devient transparent
        alpha = 1 - (self.rayon / self.rayon_max)
        if alpha > 0.5:
            pyxel.circ(self.x, self.y, self.rayon, self.couleur)
        pyxel.circb(self.x, self.y, self.rayon, 7)


class Bombe:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 60  # 2 secondes à 30 FPS
        self.exploded = False
        self.active = True
        self.particles = []
        
    def update(self):
        if not self.exploded:
            self.timer -= 1
            if self.timer <= 0:
                self.explode()
        else:
            # Met à jour les particules d'explosion
            for p in self.particles:
                p['x'] += p['dx']
                p['y'] += p['dy']
                p['vie'] -= 1
            self.particles = [p for p in self.particles if p['vie'] > 0]
            
            if len(self.particles) == 0:
                self.active = False
    
    def explode(self):
        self.exploded = True
        # Crée des particules dans toutes les directions
        for i in range(20):
            angle = (i / 20) * 2 * math.pi
            vitesse = pyxel.rndf(1, 3)
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * vitesse,
                'dy': math.sin(angle) * vitesse,
                'vie': pyxel.rndi(15, 30),
                'couleur': pyxel.rndi(8, 10)
            })
    
    def draw(self):
        if not self.exploded:
            # Bombe qui clignote
            couleur = 8 if (self.timer // 10) % 2 == 0 else 7
            pyxel.circ(self.x, self.y, 4, couleur)
            pyxel.circb(self.x, self.y, 4, 0)
            # Affiche le timer
            pyxel.text(self.x - 4, self.y - 10, str(self.timer // 30 + 1), 7)
        else:
            # Dessine les particules
            for p in self.particles:
                pyxel.pset(p['x'], p['y'], p['couleur'])


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Animations Pyxel")
        self.lasers = []
        self.cercles = []
        self.bombes = []
        self.player_x = 80
        self.player_y = 60
        pyxel.run(self.update, self.draw)
    
    def update(self):
        # Déplacement du joueur
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(5, self.player_x - 2)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(155, self.player_x + 2)
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y = max(5, self.player_y - 2)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y = min(115, self.player_y + 2)
        
        # ESPACE : Tire un laser vers le BAS
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.lasers.append(Laser(self.player_x, self.player_y, "down"))
        
        # Touches directionnelles pour tirer dans différentes directions
        if pyxel.btnp(pyxel.KEY_W):
            self.lasers.append(Laser(self.player_x, self.player_y, "up"))
        if pyxel.btnp(pyxel.KEY_A):
            self.lasers.append(Laser(self.player_x, self.player_y, "left"))
        if pyxel.btnp(pyxel.KEY_D):
            self.lasers.append(Laser(self.player_x, self.player_y, "right"))
        
        # B : Place une bombe
        if pyxel.btnp(pyxel.KEY_B):
            self.bombes.append(Bombe(self.player_x, self.player_y))
        
        # C : Crée un cercle d'expansion
        if pyxel.btnp(pyxel.KEY_C):
            self.cercles.append(CercleExpansion(self.player_x, self.player_y))
        
        # Met à jour tous les objets
        for laser in self.lasers:
            laser.update()
        self.lasers = [l for l in self.lasers if l.active]
        
        for cercle in self.cercles:
            cercle.update()
        self.cercles = [c for c in self.cercles if c.active]
        
        for bombe in self.bombes:
            bombe.update()
        self.bombes = [b for b in self.bombes if b.active]
    
    def draw(self):
        pyxel.cls(0)
        
        # Dessine tous les effets
        for cercle in self.cercles:
            cercle.draw()
        
        for laser in self.lasers:
            laser.draw()
        
        for bombe in self.bombes:
            bombe.draw()
        
        # Dessine le joueur
        pyxel.circ(self.player_x, self.player_y, 3, 11)
        
        # Instructions
        pyxel.text(5, 5, "FLECHES: Bouger", 7)
        pyxel.text(5, 12, "ESPACE: Laser BAS", 10)
        pyxel.text(5, 19, "W/A/D: Laser directions", 10)
        pyxel.text(5, 26, "C: Cercle", 8)
        pyxel.text(5, 33, "B: Bombe", 9)

App()