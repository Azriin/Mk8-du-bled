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

    def mouseOver(self):
        return -self.r <= pyxel.mouse_x - self.x <= self.r and -self.r <= pyxel.mouse_y - self.y <= self.r 
    
    def distance(self):
        return (self.x - pyxel.mouse_x)**2 + (self.y - pyxel.mouse_y)**2 

class roadBuilder:
    def __init__(self):
        self.lstRoad = [[]]
        self.radius = 16
        self.color = 13

    def draw_debug(self):
        indice = 0
        for i in range(len(self.lstRoad)):
            for j in range(len(self.lstRoad[i])):
                pyxel.text(3, 10+indice*10, f"x: {self.lstRoad[i][j].x}, y: {self.lstRoad[i][j].y}", 0)
                indice += 1

    def draw(self):
        for i in range(len(self.lstRoad)):
            for j in range(len(self.lstRoad[i])):
                self.lstRoad[i][j].draw()

    def verif_point(self, x, y):
        for i in range(len(self.lstRoad)):
            for j in range(len(self.lstRoad[i])):
                if  self.lstRoad[i][j].x == x and self.lstRoad[i][j].y == y:
                    return False
        return True

    def in_screen(self, x, y):
        x = x if x < 255-self.radius else 255-self.radius
        x = x if x > self.radius else self.radius
        y = y if y < 255-self.radius else 255-self.radius
        y = y if y > self.radius else self.radius
        return x, y

    def update(self):   
        pyxel.circb(*self.in_screen(pyxel.mouse_x, pyxel.mouse_y), self.radius, self.color)
        if pyxel.btn(pyxel.KEY_SHIFT):
            self.color = (self.color + pyxel.mouse_wheel)%16
        else : 
            rad = self.radius + pyxel.mouse_wheel
            if rad < 1:
                self.radius = 1
            elif rad > 127:
                self.radius = 127
            else: self.radius = rad

        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            x, y = self.in_screen(pyxel.mouse_x, pyxel.mouse_y)
            if self.verif_point(x, y):
                self.lstRoad[-1].append(cercle(x, y, self.radius, self.color))
        elif self.lstRoad[-1] != []:
                self.lstRoad.append([])
        elif pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.lstRoad) > 1:
            self.lstRoad.pop(-2)

    def get_road(self):
        return [element for row in self.lstRoad for element in row]
    
    def loadRoad(self, infos):
        self.lstRoad = [[]]
        for info in infos:
            self.lstRoad.append([cercle(*info)])