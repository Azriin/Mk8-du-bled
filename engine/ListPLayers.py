from engine.voitures import Car
import constante as c
import pyxel

class Lst_Cars:
    def __init__(self, nbr, map):
        self.nbr = nbr
        self.controle = [{"haut": "KEY_UP", "bas": "KEY_DOWN", "gauche": "KEY_LEFT", "droite": "KEY_RIGHT"},
                         {"haut": "KEY_Z", "bas": "KEY_S", "gauche": "KEY_Q", "droite": "KEY_D"},
                         {"haut": "KEY_O", "bas": "KEY_L", "gauche": "KEY_K", "droite": "KEY_M"},
                         {"haut": "KEY_KP_5", "bas": "KEY_KP_2", "gauche": "KEY_KP_1", "droite": "KEY_KP_3"}]
        self.coo = [(-7, -1), (-1, -7), (1, -1), (-1, 1)]
        self.lst_voitures = []
        for i in range(self.nbr):
            if (c.lst_player[i]):
                self.lst_voitures.append(Car(map[i][0]+self.coo[map[i][2]][0], map[i][1]+self.coo[map[i][2]][1], i, map[i][2]*90, None))
            else :
                self.lst_voitures.append(Car(map[i][0]+self.coo[map[i][2]][0], map[i][1]+self.coo[map[i][2]][1], i, map[i][2]*90, self.controle[i%len(self.controle)]))
        
        self.nbr_debug_car = 0

    def get_cars(self):
        return self.lst_voitures

    def draw(self):
        for car in self.lst_voitures:
            car.draw()

    def update(self, hp, parts):
        for i in range(len(self.lst_voitures)):
            self.lst_voitures[i].update(hp, parts)

    def switch_debug_car(self):
        for i in range(self.nbr):
            if eval(f"pyxel.btn(pyxel.KEY_{i+1})"):
                self.nbr_debug_car = i

    def debug(self):
        self.lst_voitures[self.nbr_debug_car].debug()

