import pyxel
import constante as c

class Car:
    def __init__(self, x, y, couleur, angle, controle):
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
        self.slow = 2
        self.delta_degre = 0
        self.delta_max = 100
        self.debut_drift = 90
        #affichage
        self.couleur = couleur
        self.controle = controle
        self.template = [[0, 8, 8],
                [8, 8, 8],
                [16, 8, 8],
                [24, 8, 8],
                [32, 8, 8],
                [40, 8, 8],
                
                [40, -8, 8],
                [32, -8, 8],
                [24, -8, 8],
                [16, -8, 8],
                [8, -8, 8],
                [0, -8, 8],
                
                [0, -8, -8],
                [8, -8, -8],
                [16, -8, -8],
                [24, -8, -8],
                [32, -8, -8],
                [40, -8, -8],
                
                [40, 8, -8],
                [32, 8, -8],
                [24, 8, -8],
                [16, 8, -8],
                [8, 8, -8],
                [0, 8, -8]]
        
        self.particulDrift = []

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
        self.draw_win(238, 2)
        pyxel.line(self.x, self.y, self.x+self.vx, self.y+self.vy, 8)
        pyxel.text(1, 1,f"""x = {self.x} | y = {self.y} 
                   \nvitesse = {self.vitesse} | Vmax = {self.Vmax} | angle = {self.degre} | movable = {"NEVER" if self.controle == None else not(self.brake)}
                    \nvx = {self.set_pas()[0]} | vy = {self.set_pas()[1]} 
                    \nsur route = {self.sur_route} | distance = {self.distance()}
                    \nmodulo = {self.degre%360} | arondie = {round(self.degre/90)*90}
                    \nidtemp = {self.degre % 360 // (360//len(self.template))} | couleur = {self.couleur}
                    \ntour = {self.lape} | partie = {self.part} |len = {len(self.course)} 
                    \ncourse = {self.course}
                    \ndist point = {self.dist}
                    \ndelta = {self.delta_degre}| drift = {abs(self.delta_degre) > self.debut_drift}
                    \n\n\n\n\n\n
                    \nA = +1 Vmax | Q = -1 Vmax
                    \nE = +1 couleur | D = -1 couleur""", 7)
        
#affichage
    def draw(self):
        indice = self.degre % 360 // (360//len(self.template))
        for coo in self.particulDrift:
            pyxel.pset(coo[0], coo[1], 0 if pyxel.pget(coo[0], coo[1]) in (13, 7, 0) else 9)
        pyxel.blt(self.x, self.y, 0, self.template[indice][0], 8*self.couleur, self.template[indice][1], self.template[indice][2], 4)
        

    def draw_win(self, x, y):
        pyxel.blt(x, y, 0, 16*self.couleur, 41, 16, 12, 4)

#son
    def playTutureVroumVroum(self):
        if abs(self.vitesse) > 0:
            pyxel.sound(4).speed = max(10-int(abs(self.vitesse))*2, 1)
            if abs(self.vitesse) == self.Vmax:
                pyxel.sound(4).set_volumes("2")
            else: pyxel.sound(4).set_volumes("1")
            if abs(self.delta_degre) > self.debut_drift:
                pyxel.sound(4).set_notes("d2")
            else: pyxel.sound(4).set_notes("c2")
            pyxel.play(0, 4)
#collision
    def distance(self):
        return ((self.vx)**2 + (self.vy)**2)**0.5

    def col_x(self, x1, x2, distance):
        return x1 < self.x + 8 + (self.vx/distance) and self.x + (self.vx/distance) < x2

    def col_y(self, y1, y2, distance):
        return y1 < self.y + 8 + (self.vy/distance) and self.y + (self.vy/distance) < y2
    
    def col_route(self):
        """
        Verifie si la voiture est sur la un pixel noir/blanc/girs(bref si c'est sur route)
        """
        val = pyxel.pget(self.x + 4 + 6 * pyxel.cos(self.degre), self.y + 4 + 6 * pyxel.sin(self.degre))
        self.sur_route = val in (13, 7, 0)

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

    def set_pas_drift(self):
        vitesse = self.vitesse
        if not(self.sur_route):
            vitesse /= self.slow
        vitesse_x = vitesse * pyxel.cos(self.degre)
        vitesse_y = vitesse * pyxel.sin(self.degre)
        facteur_drift = 1-(1/(1+abs(self.vitesse)))
        drift_x = facteur_drift * vitesse_y
        drift_y = -facteur_drift * vitesse_x
        velocite_x = vitesse_x + drift_x
        velocite_y = vitesse_y + drift_y
        # refaire les coos des particules        
        self.particulDrift.append([self.x + 1 - velocite_x, self.y + 4 - velocite_y, pyxel.frame_count])
        self.particulDrift.append([self.x + 7 - velocite_x, self.y + 4 - velocite_y, pyxel.frame_count])
        
        return [velocite_x, velocite_y]

    def actu_vecteur(self, pas):
        self.vx = pas[0]
        self.vy = pas[1]

    def move(self):
        if not(self.brake) and pyxel.btn(eval(f"pyxel.{self.controle['bas']}")):
            self.vitesse -= 1 if self.vitesse > -self.Vmax else 0
        if not(self.brake) and pyxel.btn(eval(f"pyxel.{self.controle['haut']}")):
            if self.vitesse < self.Vmax:
                self.vitesse += 1 
        if pyxel.frame_count % 10 == 0:
            if self.vitesse != 0:
                self.vitesse -= 1*pyxel.sgn(self.vitesse)
        if pyxel.btn(eval(f"pyxel.{self.controle['droite']}")):
            self.degre += 10
            self.delta_degre += 10 if self.delta_degre < self.delta_max else 0
        if pyxel.btn(eval(f"pyxel.{self.controle['gauche']}")):
            self.degre -= 10
            self.delta_degre -= 10 if self.delta_degre > -self.delta_max else 0
        if self.vitesse > 0:
            if self.delta_degre > 0:
                self.delta_degre -= abs(self.vitesse)
            elif self.delta_degre < 0:
                self.delta_degre += abs(self.vitesse)
        else: self.delta_degre = 0

#course
    def dist_point(self, point):
        """
        donne la distance entre la voiture et le la prochaine section"""
        self.dist = (((point[5][0]-self.x)**2)+((point[5][1]-self.y)**2))

    def part_actuel(self, parts):
        """
        assigne l'id de la partie ou se situe la voiture a self.part
        """
        for p in parts:
            distance = self.distance()
            if distance == 0:
                distance = 1
            if self.col_x(p[0], p[0]+p[2], distance) and self.col_y(p[1], p[1]+p[3], distance):
                self.part = p[4]

    def lst_part(self):
        """
        si la derniere partie de la course est la predeceseuse de la partie actuelle de la voiture,\n
        alors il ajoute cette partie dans self.course
        """
        if self.part == self.course[-1]+1:
            self.course.append(self.part)

    def complet_lape(self, nbr:int):
        """
        +1 a lape si la voiture est passe dans toute les partie de la course et qu'elle est revenu a la partie 0
        """
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
        # input clavier
        if (self.controle != None):
            self.move()
            self.playTutureVroumVroum()

        # calcul la les vecteurs x et y
        if abs(self.delta_degre) > self.debut_drift:
            self.actu_vecteur(self.set_pas_drift())
        else: self.actu_vecteur(self.set_pas())
        distance = self.distance()
        if distance == 0:
            distance = 1

        # les appliques si pas de colision sinon glisse contre mur
        self.try_move(hp, self.vx, 0, distance)
        self.try_move(hp, 0, self.vy, distance)

        # magie
        self.col_route()
        self.part_actuel(parts)
        self.lst_part()
        self.complet_lape(len(parts))
        self.dist_point(parts[self.course[-1]])

        # supprime les particules de drifts si existe depuis trop longtemps
        while (len(self.particulDrift) > 0 and self.particulDrift[0][2] + c.VIEPARTICULES <= pyxel.frame_count):
            self.particulDrift.pop(0)

