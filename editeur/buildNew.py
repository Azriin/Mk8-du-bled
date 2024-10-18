import pyxel
import addon_pyxel as ap

class MenuNew:
    def __init__(self, actif):
        self.actif = actif
        self.newMap = False
        self.text = ap.BigTexte(65, 87, "New map :")
        self.back = ap.TextButton(65, 114, "Back", col_in=0, col_out=1)
        self.new = ap.TextButton(143, 114, "new", col_in=12, col_out=6)

    def draw(self):
        if self.actif:
            pyxel.rect(58, 81, 139, 63, 1)
            pyxel.rect(59, 81, 138, 62, 7)
            pyxel.rect(60, 82, 136, 60, 5)
            self.text.draw()
            self.back.draw()
            self.new.draw()

    def update(self):
        if self.actif:
            self.back.animation()
            if self.back.clic():
                self.actif = False
            self.new.animation()
            if self.new.clic():
                self.newMap = True
                self.actif = False

    def getActif(self):
        return self.actif
    
    def set_actif(self, val):
        self.actif = val