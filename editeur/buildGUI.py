import addon_pyxel
import pyxel

class GUITool:
    def __init__(self):
        self.actif = True
        self.boutSelect = None
        self.cle = None
        self.bouton = {
            "save": addon_pyxel.TextButton(127, 4, "save", 6, 12),
            "quit": addon_pyxel.TextButton(194, 4, "quit", 0, 5),
            "load": addon_pyxel.TextButton(4, 4, "load", 12, 5),
            "new": addon_pyxel.TextButton(71, 4, "new", 12, 5)
        }
        self.radio = {
            "wall": addon_pyxel.Bouton_radio(6, 208, False, 15, col_out=8),
            "road": addon_pyxel.Bouton_radio(6, 234, False, 15, col_out=13),
            "deco": addon_pyxel.Bouton_radio(61, 208, False, 15, col_out=2),
            "erase": addon_pyxel.Bouton_radio(61, 234, False, 15, col_out=14),
            "separator": addon_pyxel.Bouton_radio(133, 208, False, 15),
            "dist_next": addon_pyxel.Bouton_radio(133, 234, False, 15, col_out=10),
            "starts": addon_pyxel.Bouton_radio(208, 208, False, 15, col_out=7, col_over=0)
        }
    
    def draw(self):
        if self.actif:
            pyxel.rect(0, 0, 256, 31, 1)
            pyxel.rectb(0, 0, 67, 31, 7)
            pyxel.rectb(67, 0, 56, 31, 7)
            pyxel.rectb(123, 0, 133, 31, 7)

            pyxel.rect(0, 192, 256, 64, 5)
            pyxel.rectb(0, 192, 127, 64, 7)
            pyxel.rectb(127, 192, 129, 64, 7)
            pyxel.text(2, 194, "Tools:", 7)
            pyxel.line(0, 200, 25, 200, 7)
            pyxel.line(56, 208, 56, 248, 7)
            pyxel.text(130, 194, "Road parts:", 7)
            pyxel.line(128, 200, 183, 200, 7)
            pyxel.line(202, 208, 202, 248, 7)

            pyxel.text(23, 214, "Walls", 8)
            pyxel.text(23, 240, "Roads", 13)
            pyxel.text(78, 214, "Decoration", 2)
            pyxel.text(78, 240, "Eraser", 14)
            pyxel.text(150, 214, "Separators", 0)
            pyxel.text(150, 240, "Dist next", 10)
            pyxel.text(225, 214, "Starts", 7)
            for key in self.bouton:
                self.bouton[key].draw()
            for key in self.radio:
                self.radio[key].draw()

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            pyxel.mouse(True)
            self.actif = not(self.actif)
        if self.actif:   
            for key in self.bouton:
                self.bouton[key].animation()
                if self.bouton[key].clic():
                    self.cle = None
                    self.boutSelect = key
            for key in self.radio:
                self.radio[key].actif = key == self.cle
                self.radio[key].animation()
                if self.radio[key].clic():
                    self.radio[key].reverse()
                    self.cle = key if self.cle != key else None

    def get_key(self):
        return self.cle
    
    def get_actif(self):
        return self.actif
    
    def get_boutSelect(self):
        return self.boutSelect
    
    def reset(self):
        self.boutSelect = None