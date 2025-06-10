import engine.voitures as voitures
import constante as c
import pyxel

class Ia(voitures.Car):
    def __init__(self, x, y, angle, couleur=4):
        super().__init__(x, y, couleur, angle, None)
        self.delay = c.FRAME_RATE * 0.5
        self.prevChange = 0

    def move(self, point):
        angle = int(pyxel.atan2((point[5][1]-self.y), (point[5][0]-self.x)))
        # self.degre += int(pyxel.sgn(angle) * 10)
        self.degre = angle
        
        if (pyxel.frame_count > self.prevChange + self.delay):
            self.vitesse = pyxel.rndf(2, self.Vmax)
            self.prevChange = pyxel.frame_count
        
    def update(self, hp, parts):
        if (not(self.brake)):
            self.move(parts[self.course[-1]])
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

