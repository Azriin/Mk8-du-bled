import pyxel

class Deco:
    def __init__(self, x, y, indice, rotation):
        self.x = x
        self.y = y
        self.indice = indice
        self.rotation = rotation

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16*self.indice, 240-16*self.rotation, 16, 16, 4)

    def mouseOver(self):
        return self.x <= pyxel.mouse_x < self.x+16 and self.y <= pyxel.mouse_y < self.y+16

class MenuDeco:
    def __init__(self):
        self.lstDeco = []
        self.indice = 0
        self.rotation = 0
        self.tabRota = [2, 3, 2, 4, 4, 4, 4, 4, 4, 3]
        self.mbrDecoMax = len(self.tabRota)

    def draw_debug(self):
        for i in range(len(self.lstDeco)):
            pyxel.text(3, 10+i*10, f"x: {self.lstDeco[i].x}, y: {self.lstDeco[i].y}, indice: {self.lstDeco[i].indice}, rotation: {self.lstDeco[i].rotation}", 0)

    def draw(self):
        for deco in self.lstDeco:
            deco.draw()

    def update(self):
        self.indice = (self.indice+pyxel.mouse_wheel)%self.mbrDecoMax
        x, y = pyxel.mouse_x, pyxel.mouse_y
        if pyxel.btn(pyxel.KEY_SHIFT):
                x, y = pyxel.mouse_x//16*16, pyxel.mouse_y//16*16
        if self.rotation >= self.tabRota[self.indice]:
            self.rotation = 0
        if pyxel.btnp(pyxel.KEY_R):
            self.rotation = (self.rotation+1)%self.tabRota[self.indice]
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.lstDeco.append(Deco(x, y, self.indice, self.rotation))
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.lstDeco) > 0:
            self.lstDeco.pop()
        pyxel.blt(x, y, 0, 16*self.indice, 240-16*self.rotation, 16, 16, 4)

    def get_deco(self):
        return self.lstDeco

    def loadDeco(self, infos):
        self.lstDeco = []
        for info in infos:
            self.lstDeco.append(Deco(*info))