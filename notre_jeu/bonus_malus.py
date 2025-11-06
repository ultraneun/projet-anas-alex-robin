import pyxel
import random


class BonusMalus:

	def __init__(self, explosion_callback=None):
		self.coeurs_liste = []
		self.meteores_liste = []
		self.explosion_callback = explosion_callback


	def update(self):
		# spawn coeur (rare)
		if pyxel.frame_count % 150 == 0:
			self.coeurs_liste.append([random.randint(0, 120), 0])

		# spawn météorite (plus fréquent)
		if pyxel.frame_count % 20 == 0:
			self.meteores_liste.append([random.randint(0, 120), 0])

		# déplacement : descend
		self.coeurs_liste = [[x, y + 1] for x, y in self.coeurs_liste if y + 1 <= 140]
		self.meteores_liste = [[x, y + 2] for x, y in self.meteores_liste if y + 2 <= 140]

	def check_player_collision(self, vaisseau_x, vaisseau_y):
		"""Vérifie collisions avec le vaisseau.

		Retourne un entier : delta de vies (positif si coeur, négatif si météorite).
		On supprime les éléments touchés.
		"""
		delta_vies = 0

		# coeurs
		coeurs_to_remove = set()
		for i, coeur in enumerate(self.coeurs_liste):
			if (coeur[0] <= vaisseau_x + 8 and coeur[0] + 8 >= vaisseau_x and
					coeur[1] <= vaisseau_y + 8 and coeur[1] + 8 >= vaisseau_y):
				delta_vies += 1
				coeurs_to_remove.add(i)

		# meteores
		meteores_to_remove = set()
		for i, meteore in enumerate(self.meteores_liste):
			if (meteore[0] <= vaisseau_x + 8 and meteore[0] + 8 >= vaisseau_x and
					meteore[1] <= vaisseau_y + 8 and meteore[1] + 8 >= vaisseau_y):
				delta_vies -= 1
				meteores_to_remove.add(i)
				# créer explosion via callback si fournie
				if self.explosion_callback:
					self.explosion_callback(meteore[0], meteore[1])

		if coeurs_to_remove:
			self.coeurs_liste = [c for idx, c in enumerate(self.coeurs_liste) if idx not in coeurs_to_remove]
		if meteores_to_remove:
			self.meteores_liste = [m for idx, m in enumerate(self.meteores_liste) if idx not in meteores_to_remove]

		return delta_vies

	def draw(self):
		"""Dessine les coeurs et météorites de manière simple (cercles/rectangles)."""
		# coeurs (rose/rouge)
		for c in self.coeurs_liste:
			pyxel.blt(c[0], c[1], 0, 8, 16, 8, 8, 0)  # sprite coeur


		# météorites (gris)
		for m in self.meteores_liste:
			pyxel.blt(m[0], m[1], 0, 16, 8, 8, 8, 0)  # sprite météorite


