import pyxel

class Erase:
    def __init__(self, tool):
        self.tool = tool

    def inRoad(self):
        toDel = [None, -1, 4096]
        for i in range(len(self.tool["road"].lstRoad)):
            for road in self.tool["road"].lstRoad[i]:
                if (road.mouseOver() and road.distance() < toDel[2]):
                    toDel[0] = road
                    toDel[1] = i
                    toDel[2] = road.distance()
        if (toDel[0] != None):
            self.tool["road"].lstRoad[toDel[1]].remove(toDel[0])
            return True
        return False

    def inWall(self):
        for mur in self.tool["wall"].lstMurs:
            if (mur.mouseOver()):
                self.tool["wall"].lstMurs.remove(mur)
                return True
        return False

    def inDeco(self):
        for deco in self.tool["deco"].get_deco():
            if (deco.mouseOver()):
                self.tool["deco"].lstDeco.remove(deco)
                return True
        return False

    def search(self):
        if (self.inDeco()): return
        if (self.inWall()): return
        if (self.inRoad()): return
        
    def draw(self):
        pass

    def draw_debug(self):
        pass

    def update(self):
        pyxel.mouse(False)
        pyxel.rectb(pyxel.mouse_x-1, pyxel.mouse_y-1, 3, 3, 7)
        if ((pyxel.btn(pyxel.KEY_SHIFT) and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)) or (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT))):
            self.search()