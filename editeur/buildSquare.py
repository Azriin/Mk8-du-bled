import pyxel

class Carre:
    def __init__(self, plein, col=8, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
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
        self.x1 = max(self.x1, 0)
        self.y1 = max(self.y1, 0)
        self.x2 = min(256, self.x2)
        self.y2 = min(256, self.y2)

    def carre(self, x1, y1, x2, y2):
        sign_x = -1 if x2 < x1 else 1
        sign_y = -1 if y2 < y1 else 1
        x2 = x1 + sign_x * abs(y2 - y1)
        y2 = y1 + sign_y * abs(x2 - x1)
        self.reorder(x1, y1, x2, y2)

    def update(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and not(self.stateMouse):
            self.stateMouse = True
            self.x1 = self.saveX = pyxel.mouse_x
            self.y1 = self.saveY = pyxel.mouse_y
        elif pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and self.stateMouse:
            if pyxel.btn(pyxel.KEY_SHIFT):
                #a re faire
                self.carre(self.saveX, self.saveY, pyxel.mouse_x, pyxel.mouse_y)
            else : self.reorder(self.saveX, self.saveY, pyxel.mouse_x, pyxel.mouse_y)

class CreationMurs:
    def __init__(self):
        self.color = 8
        self.lstMurs = []

    def draw(self):
        for mur in self.lstMurs:
            mur.draw()
    
    def draw_debug(self):
        for i in range(len(self.lstMurs)):
            pyxel.text(3, 10+i*10, f"""x1: {self.lstMurs[i].x1}, y1: {self.lstMurs[i].y1}, x2: {self.lstMurs[i].x2}, y2: {self.lstMurs[i].y2}""", 0)

    def update(self):
        pyxel.rectb(pyxel.mouse_x-4, pyxel.mouse_y-4, 8, 8, self.color)
        self.color = (self.color + pyxel.mouse_wheel)%16
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.lstMurs) != 0:
            self.lstMurs.pop()
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.lstMurs.append(Carre(True, self.color))
        if len(self.lstMurs) != 0:
            self.lstMurs[-1].update()

    def loadMurs(self, infos):
        self.lstMurs = []
        for info in infos:
            col = 8 if len(info) == 4 else info[4]
            self.lstMurs.append(Carre(True, col=col, x1=info[0], y1=info[1], x2=info[0]+info[2], y2=info[1]+info[3]))

class CreationSep:
    def __init__(self):
        self.lstSep = []

    def draw(self):
        for sep in self.lstSep:
            sep.draw()
    
    def draw_debug(self):
        for i in range(len(self.lstSep)):
            pyxel.text(3, 10+i*10, f"x1: {self.lstSep[i].x1}, y1: {self.lstSep[i].y1}, x2: {self.lstSep[i].x2}, y2: {self.lstSep[i].y2}", 0)

    def update(self, lstPoints):
        pyxel.rectb(pyxel.mouse_x-4, pyxel.mouse_y-4, 8, 8, len(self.lstSep)%16)
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.lstSep) != 0:
            self.lstSep.pop()
            i = 0
            while i < len(lstPoints):
                if lstPoints[i].part == len(self.lstSep):
                    lstPoints.pop(i)
                    break
                i += 1
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.lstSep.append(Carre(False, len(self.lstSep)%16))
        if len(self.lstSep) != 0:
            self.lstSep[-1].update()

    def getLst(self):
        return self.lstSep
    
    def loadSep(self, infos):
        self.lstSep = []
        for info in infos:
            self.lstSep.append(Carre(False, col=info[4], x1=info[0], y1=info[1], x2=info[0]+info[2], y2=info[1]+info[3]))