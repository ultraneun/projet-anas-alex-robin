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