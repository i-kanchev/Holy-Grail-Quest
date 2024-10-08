import copy

from character import *
from ability import *

#knight class
class Knight(Character):
    def __init__(self, x, y, name, max_hp, strength, abilities:list):
        super().__init__(x, y, name, max_hp, strength)
        self.abilities = []
        for ability in abilities:
            self.abilities.append(copy.copy(ability))

    def pass_turn(self):
        super()
        for ability in self.abilities:
            ability.reduce_cd()

    def heal_pot(self):
        self.hp = min(self.hp + 30, self.max_hp)

    def draw_abilities(self):
        for ability in self.abilities:
            ability.draw()

