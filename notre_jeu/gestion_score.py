import pyxel

class GestionScore:
    def __init__(self):
        self.score = 0
        self.vies = 3
        self.bonus_actif = False
        self.timer_bonus = 0

    def ajouter_score(self, points):
        self.score += points

    def retirer_vie(self):
        self.vies -= 1

    def activer_bonus(self, duree):
        self.bonus_actif = True
        self.timer_bonus = duree

    def update(self):
        # gestion du temps de bonus
        if self.bonus_actif:
            self.timer_bonus -= 1
            if self.timer_bonus <= 0:
                self.bonus_actif = False

    def draw(self):
        pyxel.text(5, 5, f"Score : {self.score}", 7)
        pyxel.text(5, 15, f"Vies : {self.vies}", 8)
        if self.bonus_actif:
            pyxel.text(60, 5, "BONUS !", 10)
