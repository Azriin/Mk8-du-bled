import pyxel

class Carre:
    def __init__(self, plein, col=8):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.saveX = 0
        self.saveY = 0
        self.col = col
        self.plein = plein
        self.stateMouse = False

    def draw(self):
        if self.plein:
            pyxel.rect(self.x1, self.y1, self.x2-self.x1, self.y2-self.y1, self.col)
        else:
            pyxel.rectb(self.x1, self.y1, self.x2-self.x1, self.y2-self.y1, self.col)

    def reorder(self, x1, y1, x2, y2):
        self.x1, self.x2 = (x1, x2) if x1 < x2 else (x2, x1)
        self.y1, self.y2 = (y1, y2) if y1 < y2 else (y2, y1)

    def update(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and not(self.stateMouse):
            self.stateMouse = True
            self.x1 = self.saveX = pyxel.mouse_x
            self.y1 = self.saveY = pyxel.mouse_y
        elif pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.stateMouse:
            self.reorder(self.saveX, self.saveY, pyxel.mouse_x, pyxel.mouse_y)

class CreationMurs:
    def __init__(self):
        self.lstMurs = []

    def draw(self):
        for mur in self.lstMurs:
            mur.draw()
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.lstMurs) != 0:
            self.lstMurs.pop()
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.lstMurs.append(Carre(True))
        if len(self.lstMurs) != 0:
            self.lstMurs[-1].update()

class CreationSep:
    def __init__(self):
        self.lstSep = []

    def draw(self):
        for sep in self.lstSep:
            sep.draw()
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.lstSep) != 0:
            self.lstSep.pop()
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.lstSep.append(Carre(False, len(self.lstSep)%16))
        if len(self.lstSep) != 0:
            self.lstSep[-1].update()

    def getLst(self):
        return self.lstSep