import pyxel
import constante as c

class start:
    def __init__(self, x, y, indice):
        self.x = x
        self.y = y
        self.indice = indice
        self.angle = [(1, 0, 1, 5, 0, 0, 0, 5), 
                      (0, 1, 5, 1, 0, 0, 5, 0),
                      (0, 0, 0, 5, 1, 0, 1, 5),
                      (0, 0, 5, 0, 0, 1, 5, 1)][indice]#0->E, 1->S, 2->O, 3->N

    def draw(self):
        pyxel.line(self.x+self.angle[0], self.y+self.angle[1], self.x+self.angle[2], self.y+self.angle[3], 7)
        pyxel.pset(self.x+self.angle[4], self.y+self.angle[5], 7)
        pyxel.pset(self.x+self.angle[6], self.y+self.angle[7], 7)

class CreationStart:
    def __init__(self):
        self.lstStart = [start(3*i, 0, 0) for i in range(c.max_player)]
        self.angle = 0

    def draw(self):
        for start in self.lstStart:
            start.draw()

    def draw_debug(self):
        for i in range(len(self.lstStart)):
            pyxel.text(3, 10+i*10, f"x: {self.lstStart[i].x}, y: {self.lstStart[i].y}, angle: {self.lstStart[i].angle}", 0)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if len(self.lstStart) == c.max_player:
                self.lstStart.pop(0)
            self.lstStart.append(start(pyxel.mouse_x, pyxel.mouse_y, self.angle))
        elif pyxel.btnp(pyxel.KEY_R):
            self.angle = (self.angle + 1)% 4

    def loadStart(self, infos):
        self.lstStart = []
        for info in infos:
            self.lstStart.append(start(*info))