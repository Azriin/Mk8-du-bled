import pyxel

class Walls:
    def __init__(self, lape):
        self.bordure = lape

    def get_hp(self):
        return self.bordure

    def draw(self):
        for i in range(len(self.bordure)):
            if len(self.bordure[i]) == 4:
                pyxel.rect(*self.bordure[i], 8)
            else : pyxel.rect(*self.bordure[i])