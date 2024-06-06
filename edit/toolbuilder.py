import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# #-----------------------------------------------------------------------------#
import addon_pyxel
import pyxel

class GUITool:
    def __init__(self):
        self.actif = False
        self.cle = None
        self.boutonSave = addon_pyxel.TextButton(194, 212, "save", 6, 12)
        self.radio = {"wall": addon_pyxel.Bouton_radio(6, 208, False, 15, col_out=8),
                      "road": addon_pyxel.Bouton_radio(6, 234, False, 15, col_out=13),
                      "separator": addon_pyxel.Bouton_radio(70, 208, False, 15),
                      "dist next": addon_pyxel.Bouton_radio(70, 234, False, 15, col_out=10)}

    
    def draw(self):
        if self.actif:
            pyxel.rect(0, 192, 256, 64, 5)
            pyxel.rectb(0, 192, 64, 64, 7)
            pyxel.rectb(64, 192, 192, 64, 7)
            pyxel.rectb(192, 193, 63, 62, 7)
            pyxel.line(191, 193, 191, 254, 7)
            pyxel.text(2, 194, "Tools:", 7)
            pyxel.line(0, 200, 25,200, 7)
            pyxel.text(67, 194, "Road parts:", 7)
            pyxel.line(65, 200, 110,200, 7)

            pyxel.text(23, 214, "Walls", 8)
            pyxel.text(23, 240, "Roads", 13)
            pyxel.text(87, 214, "Separators", 0)
            pyxel.text(87, 240, "Dist next", 10)
            self.boutonSave.draw()
            for key in self.radio:
                self.radio[key].draw()

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.actif = not(self.actif)
        if self.actif:
            self.boutonSave.animation()
            if self.boutonSave.clic():
                pass
            for key in self.radio:
                self.radio[key].actif = key == self.cle
                self.radio[key].animation()
                if self.radio[key].clic():
                    self.radio[key].reverse()
                    self.cle = key if self.cle != key else None
                    self.actif = False


    def get_key(self):
        return self.cle
    
    def get_actif(self):
        return self.actif