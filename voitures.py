import pyxel

class Car:
    def __init__(self, x, y, couleur, angle, controle, mode_facile):
        #course
        self.dist = 0
        self.lape = 0
        self.part = 0
        self.course = [0]
        #deplacement
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.vitesse = 0
        self.Vmax = 3
        self.degre = angle
        self.brake = False
        self.sur_route = True
        self.slow = 1.5
        self.mode_facile = mode_facile
        #affichage
        self.couleur = couleur
        self.controle = controle
        self.template = ["pyxel.blt(self.x, self.y, 0, 0, 8*self.couleur, 8, 8, 4)",
                "pyxel.blt(self.x, self.y, 0, 8, 8*self.couleur, 8, 8, 4)",
                "pyxel.blt(self.x, self.y, 0, 16, 8*self.couleur, 8, 8, 4)",
                "pyxel.blt(self.x, self.y, 0, 24, 8*self.couleur, 8, 8, 4)",
                "pyxel.blt(self.x, self.y, 0, 32, 8*self.couleur, 8, 8, 4)",
                "pyxel.blt(self.x, self.y, 0, 40, 8*self.couleur, 8, 8, 4)",
                
                "pyxel.blt(self.x, self.y, 0, 40, 8*self.couleur, -8, 8, 4)",
                "pyxel.blt(self.x, self.y, 0, 32, 8*self.couleur, -8, 8, 4)",
                "pyxel.blt(self.x, self.y, 0, 24, 8*self.couleur, -8, 8, 4)",
                "pyxel.blt(self.x, self.y, 0, 16, 8*self.couleur, -8, 8, 4)",
                "pyxel.blt(self.x, self.y, 0, 8, 8*self.couleur, -8, 8, 4)",
                "pyxel.blt(self.x, self.y, 0, 0, 8*self.couleur, -8, 8, 4)",
                
                "pyxel.blt(self.x, self.y, 0, 0, 8*self.couleur, -8, -8, 4)",
                "pyxel.blt(self.x, self.y, 0, 8, 8*self.couleur, -8, -8, 4)",
                "pyxel.blt(self.x, self.y, 0, 16, 8*self.couleur, -8, -8, 4)",
                "pyxel.blt(self.x, self.y, 0, 24, 8*self.couleur, -8, -8, 4)",
                "pyxel.blt(self.x, self.y, 0, 32, 8*self.couleur, -8, -8, 4)",
                "pyxel.blt(self.x, self.y, 0, 40, 8*self.couleur, -8, -8, 4)",
                
                "pyxel.blt(self.x, self.y, 0, 40, 8*self.couleur, 8, -8, 4)",
                "pyxel.blt(self.x, self.y, 0, 32, 8*self.couleur, 8, -8, 4)",
                "pyxel.blt(self.x, self.y, 0, 24, 8*self.couleur, 8, -8, 4)",
                "pyxel.blt(self.x, self.y, 0, 16, 8*self.couleur, 8, -8, 4)",
                "pyxel.blt(self.x, self.y, 0, 8, 8*self.couleur, 8, -8, 4)",
                "pyxel.blt(self.x, self.y, 0, 0, 8*self.couleur, 8, -8, 4)",]
#debug
    def debug(self):
        if pyxel.btnp(pyxel.KEY_A):#vmax
            self.Vmax += 1
        if pyxel.btnp(pyxel.KEY_Q):
            self.Vmax -= 1 if self.Vmax > 0 else 0

        if pyxel.btnp(pyxel.KEY_E):#couleur
            self.couleur += 1 if self.couleur < 4 else 0
        if pyxel.btnp(pyxel.KEY_D):
            self.couleur -= 1 if self.couleur > 0 else 0
        # pyxel.pset(self.x+4 + 6 * pyxel.cos(self.degre), self.y+4 + 6 * pyxel.sin(self.degre), 7)
        self.draw_win(238, 2)
        pyxel.text(1, 1,f"""x = {self.x} | y = {self.y} 
                   \nvitesse = {self.vitesse} | Vmax = {self.Vmax} | angle = {self.degre} | brake = {self.brake}
                    \nvx = {self.set_pas()[0]} | vy = {self.set_pas()[1]} 
                    \nsur route = {self.sur_route} | distance = {self.distance()}
                    \nmodulo = {self.degre%360} | arondie = {round(self.degre/90)*90}
                    \nidtemp = {self.degre % 360 // (360//len(self.template))} | couleur = {self.couleur}
                    \ntour = {self.lape} | partie = {self.part} |len = {len(self.course)} 
                    \ncourse = {self.course}
                    \ndist point = {self.dist}""", 7)
        
        pyxel.text(1, 238, """A = +1 Vmax | Q = -1 Vmax
                   \nE = +1 couleur | D = -1 couleur""", 7)
#affichage
    def draw(self):
        indice = self.degre % 360 // (360//len(self.template))
        eval(self.template[indice])

    def draw_win(self, x, y):
        pyxel.blt(x, y, 0, 16*self.couleur, 41, 16, 12, 4)
#collision
    def distance(self):
        return ((self.vx)**2 + (self.vy)**2)**0.5

    def col_x(self, x1, x2, distance):
        return x1 < self.x + 8 + (self.vx/distance) and self.x + (self.vx/distance) < x2

    def col_y(self, y1, y2, distance):
        return y1 < self.y + 8 + (self.vy/distance) and self.y + (self.vy/distance) < y2
    
    def col_route(self):
        self.sur_route = (pyxel.pget(self.x+4 + 6 * pyxel.cos(self.degre), self.y+4 + 6 * pyxel.sin(self.degre))) == 13 \
                      or (pyxel.pget(self.x+4 + 6 * pyxel.cos(self.degre), self.y+4 + 6 * pyxel.sin(self.degre))) == 7  \
                      or (pyxel.pget(self.x+4 + 6 * pyxel.cos(self.degre), self.y+4 + 6 * pyxel.sin(self.degre))) == 0  
#deplacement
    def reverse_brake(self, val=None):
        if val == None:
            self.brake = not(self.brake)
        else: self.brake = val

    def try_move(self, hp, vx, vy, distance):
        self.x += vx
        self.y += vy
        for elt in hp:
            if self.col_x(elt[0], elt[0]+elt[2], distance) and self.col_y(elt[1], elt[1]+elt[3], distance):
                self.x -= vx
                self.y -= vy

    def set_pas(self):
        #[vx ,vy]
        vitesse = self.vitesse
        if not(self.sur_route):
            vitesse /= self.slow
        return [vitesse * (pyxel.cos(self.degre)), vitesse * (pyxel.sin(self.degre))]

    def actu_vecteur(self, pas):
        self.vx = pas[0]
        self.vy = pas[1]

    def move(self):
        if not(self.brake):
            if pyxel.btn(eval(f"pyxel.{self.controle['bas']}")):
                self.vitesse -= 1 if self.vitesse > -self.Vmax else 0
            if pyxel.btn(eval(f"pyxel.{self.controle['haut']}")):
                if self.vitesse < self.Vmax:
                    self.vitesse += 1 
                elif self.mode_facile:
                    self.degre = round(self.degre/90)*90
            elif not(self.mode_facile):
                if pyxel.frame_count % 10 == 0:
                    if self.vitesse != 0:
                        self.vitesse -= 1*pyxel.sgn(self.vitesse)
        if pyxel.btn(eval(f"pyxel.{self.controle['droite']}")):
            self.degre += 10
        if pyxel.btn(eval(f"pyxel.{self.controle['gauche']}")):
            self.degre -= 10
#course
    def dist_point(self, point):
        self.dist = (((point[5][0]-self.x)**2)+((point[5][1]-self.y)**2))

    def part_actuel(self, parts):
        for p in parts:
            distance = self.distance()
            if distance == 0:
                distance = 1
            if self.col_x(p[0], p[0]+p[2], distance) and self.col_y(p[1], p[1]+p[3], distance):
                self.part = p[4]

    def lst_part(self):
        if self.part == self.course[-1]+1:
            self.course.append(self.part)

    def complet_lape(self, nbr):
        if self.part != self.course[-1] and len(self.course) == nbr and self.part == 0:
            self.course = [0]
            self.lape += 1

    def get_lape(self):
        return self.lape
    
    def get_part(self):
        return self.course[-1]
    
    def get_col(self):
        return self.couleur
    
    def get_dist(self):
        return self.dist
#update
    def update(self, hp, parts):
        self.move()
        self.actu_vecteur(self.set_pas())
        distance = self.distance()
        if distance == 0:
            distance = 1
        self.try_move(hp, self.vx, 0, distance)
        self.try_move(hp, 0, self.vy, distance)
        self.col_route()
        self.part_actuel(parts)
        self.lst_part()
        self.complet_lape(len(parts))
        self.dist_point(parts[self.course[-1]])


class Lst_Cars:
    def __init__(self, nbr, gm, map):
        assert nbr <= 5
        self.nbr = nbr
        self.gm = gm
        self.info = [{"angle": 0, "x": "70-8*i", "y":"210 if i%2==0 else 226"},
                     {"angle": 180, "x": "132+8*i", "y":"12 if i%2==0 else 28"},
                     {"angle": 180, "x": "146+8*i", "y": "210 if i%2==0 else 222"}]
        self.controle = [{"haut": "KEY_UP", "bas": "KEY_DOWN", "gauche": "KEY_LEFT", "droite": "KEY_RIGHT"},
                         {"haut": "KEY_Z", "bas": "KEY_S", "gauche": "KEY_Q", "droite": "KEY_D"},
                         {"haut": "KEY_O", "bas": "KEY_L", "gauche": "KEY_K", "droite": "KEY_M"},
                         {"haut": "KEY_KP_5", "bas": "KEY_KP_2", "gauche": "KEY_KP_1", "droite": "KEY_KP_3"}]
        self.lst_voitures = [Car(eval(self.info[map]["x"]), eval(self.info[map]["y"]), i, self.info[map]["angle"], self.controle[i%len(self.controle)], self.gm) for i in range(self.nbr)]
        self.nbr_debug_car = 0

    def get_cars(self):
        return self.lst_voitures

    def draw(self):
        for car in self.lst_voitures:
            car.draw()

    def update(self, hp, parts):
        for car in self.lst_voitures:
            car.update(hp, parts)

    def switch_debug_car(self):
        for i in range(self.nbr):
            if eval(f"pyxel.btn(pyxel.KEY_{i+1})"):
                self.nbr_debug_car = i

    def debug(self):
        self.lst_voitures[self.nbr_debug_car].debug()