import pyxel
import constante as c

class Lape:
    def __init__(self, lape):
        self.separateur = lape

    def get_part(self):
        return self.separateur

    def draw(self):
        for i in range(len(self.separateur)):
            pyxel.rectb(*self.separateur[i][:4], col=self.separateur[i][4]%16)