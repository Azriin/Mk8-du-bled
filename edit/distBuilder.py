import pyxel

class Point:
    def __init__(self, x, y, part):
        self.x = x
        self.y = y
        self.part = part

    def draw(self):
        pyxel.pset(self.x, self.y, 15)

    def getVal(self):
        return self.x, self.y, self.part

class CreationPoint:
    def __init__(self):
        self.lstPoint = []

    def draw(self):
        # i = 0
        for point in self.lstPoint:
            point.draw()
            # pyxel.text(0, 10*i, str(point.getVal()), 0)
            # i += 1

    def update(self, lstSec):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x, y = pyxel.mouse_x, pyxel.mouse_y
            secCourante = self.verifSection(x, y, lstSec)
            if secCourante != -1:
                self.lstPoint.append(Point(*self.adjustCoo(x, y, lstSec[secCourante]), secCourante))
            else: print("pas de section")
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
        
        # Trouver la distance minimale
        min_dist = min(dist_to_left, dist_to_right, dist_to_top, dist_to_bottom)
        
        # Ajuster les coordonnées du point pour le placer sur le côté le plus proche
        if min_dist == dist_to_left:
            x = part.x1
        elif min_dist == dist_to_right:
            x = part.x2-1
        elif min_dist == dist_to_top:
            y = part.y1
        elif min_dist == dist_to_bottom:
            y = part.y2-1
        
        return (x, y)