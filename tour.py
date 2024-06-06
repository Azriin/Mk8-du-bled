import pyxel

class Lape:
    def __init__(self, players, lape, max_lape):
                            #x, y, w, h, num, (point_dist(x, y))
        self.separateur = lape.get_separateur()
        self.max_lape = max_lape
        self.players = players

    def verif_lape(self):
        for player in self.players:
            if player.get_lape() == self.max_lape:
                return (True, player.get_col())
        return (False, None)

    def get_maxl(self):
        return self.max_lape

    def get_part(self):
        return self.separateur

    def draw(self):
        for i in range(len(self.separateur)):
            pyxel.rectb(*self.separateur[i][:4], col=self.separateur[i][4]%16)