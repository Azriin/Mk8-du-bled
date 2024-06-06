import pyxel

class cercle:
    def __init__(self, x, y, r=16, col=13):
        self.x = x
        self.y = y
        self.r = r
        self.col = col

    def getCoo(self):
        return self.x, self.y

    def draw(self):
        pyxel.circ(self.x, self.y, self.r, self.col)

class roadBuilder:
    def __init__(self):
        self.lstRoad = [[]]

    def draw(self):
        for i in range(len(self.lstRoad)):
            for j in range(len(self.lstRoad[i])):
                self.lstRoad[i][j].draw()

    def update(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.lstRoad[-1].append(cercle(pyxel.mouse_x, pyxel.mouse_y))
        elif self.lstRoad[-1] != []:
                self.lstRoad.append([])
        elif pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.lstRoad) > 1:
            self.lstRoad.pop(-2)