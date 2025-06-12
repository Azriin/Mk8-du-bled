import pyxel

class Point:
    def __init__(self, x, y, part):
        self.x = x
        self.y = y
        self.part = part

    def draw(self):
        pyxel.pset(self.x, self.y, 15)

class CreationPoint:
    def __init__(self):
        self.lstPoint = []

    def draw(self):
        for point in self.lstPoint:
            point.draw()

    def draw_debug(self):
        for i in range(len(self.lstPoint)):
            pyxel.text(3, 10+i*10, f"x: {self.lstPoint[i].x}, y: {self.lstPoint[i].y}", 0)

    def update(self, lstSec):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            x, y = pyxel.mouse_x, pyxel.mouse_y
            secCourante = self.verifSection(x, y, lstSec)
            if secCourante != -1:
                self.lstPoint = [p for p in self.lstPoint if p.part != secCourante]
                self.lstPoint.append(Point(*self.adjustCoo(x, y, lstSec[secCourante]), secCourante))
        elif pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.lstPoint) > 0:
            self.lstPoint.pop()

    def verifSection(self, x, y, lstSec):
        for i in range(len(lstSec)):
            if lstSec[i].x1 <= x <= lstSec[i].x2 and lstSec[i].y1 <= y <= lstSec[i].y2:
                return i
        return -1
    
    def adjustCoo(self, x, y, part):
        dist_to_left = abs(x - part.x1)
        dist_to_right = abs(x - part.x2)
        dist_to_top = abs(y - part.y1)
        dist_to_bottom = abs(y - part.y2)
        min_dist = min(dist_to_left, dist_to_right, dist_to_top, dist_to_bottom)
        if min_dist == dist_to_left:
            x = part.x1
        elif min_dist == dist_to_right:
            x = part.x2-1
        elif min_dist == dist_to_top:
            y = part.y1
        elif min_dist == dist_to_bottom:
            y = part.y2-1
        return (x, y)
    
    def loadDist(self, infos):
        self.lstPoint = [Point(info[5][0], info[5][1], info[4]) for info in infos]