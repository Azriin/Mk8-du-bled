import pyxel
import engine.tour as tour
import engine.mur as mur
import editeur.buildStart as buildStart
import editeur.buildDeco as buildDeco

class Load:
    def __init__(self, fichier):
        i = 0
        self.info = [[], [], [], [], []]
        with open(f"maps/{fichier}", "r") as file:
            for ligne in file:
                if ligne.strip() == '':
                    i += 1
                else:
                    self.info[i].append(eval(ligne[:-1]))
        self.murs = mur.Walls(self.info[1])
        self.tour = tour.Lape(self.info[2])
        self.starts = [buildStart.start(*elt) for elt in self.info[3]]
        self.deco = [buildDeco.Deco(*elt) for elt in self.info[4]]
        self.fichier = fichier

    def get_fichier(self):
        return self.fichier

    def get_route(self):
        return self.info[0]
    
    def get_bordure(self):
        return self.info[1]
    
    def get_separateur(self):
        return self.info[2]
    
    def get_starts(self):
        return self.info[3]
    
    def get_deco(self):
        return self.info[4]

    def draw_info(self):
        for i in range(len(self.info)):
            print(self.info[i])

    def draw(self):
        for route in self.info[0]:
            pyxel.circ(*route)
        self.murs.draw()
        for start in self.starts:
            start.draw()
        for deco in self.deco:
            deco.draw()

    def drawDebug(self):
        self.tour.draw()
