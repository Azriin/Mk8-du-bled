import pyxel
import loadMap

class Visu:
    def __init__(self, file, ratio):
        self.ratio = ratio
        self.map = loadMap.Load(file)
        self.map_ratio = [self.map.get_route(), self.map.get_bordure()]
        self.map_ratio = self.divise_matrice(self.map_ratio, self.ratio)

    def get_map(self):
        return self.map
    
    def set_map(self, file):
        self.map = loadMap.Load(file)
        self.map_ratio = [self.map.get_route(), self.map.get_bordure()]
        self.map_ratio = self.divise_matrice(self.map_ratio, self.ratio)

    def divise_matrice(self, matrice, diviseur):
        for i in range(len(matrice)):
            for j in range(len(matrice[i])):
                matrice[i][j] = list(elem // diviseur for elem in matrice[i][j])
        return matrice

    def draw(self, x, y):
        pyxel.rect(x, y, 256//self.ratio-2, 256//self.ratio-2, 11)
        for road in self.map_ratio[0]:
            if len(road) != 4:
                pyxel.circ(x+road[0]-1, y+road[1]-1, int(16//self.ratio)-1, 13)
            else: 
                pyxel.circ(x+road[0]-1, y+road[1]-1, int(road[2]), 13)
        for wall in self.map_ratio[1]:            
            pyxel.rect(x+wall[0], y+wall[1], wall[2], wall[3], 8)
