import pyxel

class Walls:
    def __init__(self, lape): #x, y, w, h
        self.bordure = lape.get_bordure()

    def get_hp(self):
        return self.bordure

    def draw(self):
        for i in range(len(self.bordure)):
            pyxel.rect(*self.bordure[i], 8)