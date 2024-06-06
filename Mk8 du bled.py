import pyxel
import voitures
import mur
import tour
import gui
import maps

max_lape = 1
nbr_joueur = 1
mode_facile = False

class App:
    def __init__(self):
        pyxel.init(256, 256, "Mk8 du bled", fps=30)
        pyxel.image(0).load(0, 0, "images/images.png")
        pyxel.image(1).load(0, 0, "images/course_1.png")
        #voitures
        self.voiture = voitures.Lst_Cars(nbr_joueur, mode_facile, 1)
        #
        self.carte = maps.Course_1()
        #colisions
        self.colision = mur.Walls(self.carte)
        #jeu
        self.tour = tour.Lape(self.voiture.get_cars(), self.carte, max_lape)
        #gui
        self.menu = gui.Menu(True)
        self.gm = gui.GameMode()
        self.victoire = gui.Victoire(self.voiture.get_cars(), False)
        self.in_game = gui.In_game(self.voiture.get_cars())
        self.chosemaps = gui.ChoseMaps()
        #debug
        self.debug_menu = False

        pyxel.run(self.draw, self.update)
        
    def actu_map(self, indice):
        pyxel.image(1).load(0, 0, f"images/course_{indice}.png")

    def update(self):
        if self.menu.get_affiche():#menu principale
            self.menu.update()
            pyxel.mouse(True)

        elif self.victoire.get_affiche():#victoire
            self.victoire.update(self.menu)
            pyxel.mouse(True)
            if self.victoire.back.clic():
                self.gm.affiche = True
                
        elif self.gm.get_affiche():#gm
            pyxel.mouse(True)
            self.gm.update(self.menu, self.chosemaps, self.chosemaps.get_selection())
            if self.gm.jouer.clic():
                info = self.gm.rtn_info()
                self.actu_map(self.carte.get_indice())
                self.voiture = voitures.Lst_Cars(info[0], info[1], self.carte.get_indice()-1)
                self.tour = tour.Lape(self.voiture.get_cars(), self.carte, info[2])
                self.colision = mur.Walls(self.carte)
                self.in_game.restart(self.voiture.get_cars())
                self.victoire.actu_players(self.voiture.get_cars())

        elif self.chosemaps.get_affiche():#selecteur maps
            pyxel.mouse(True)
            self.chosemaps.update(self.gm)
            selection = self.chosemaps.get_selection()
            if selection == 0:
                selection = pyxel.rndi(1, self.chosemaps.get_display_maps()-1)
            self.carte = eval(f"maps.Course_{selection}()")

        else:#en jeu
            pyxel.mouse(False)
            if self.tour.verif_lape()[0]:
                self.victoire.reverse()
            else:
                self.voiture.update(self.colision.get_hp(), self.tour.get_part())
                self.in_game.update()
                #debug
                if pyxel.btnp(pyxel.KEY_B):
                        self.debug_menu = not(self.debug_menu)
                if self.debug_menu:
                    self.voiture.switch_debug_car()

    def draw(self):
        pyxel.cls(7)
        if self.menu.get_affiche():
            self.menu.draw()
        elif self.victoire.get_affiche():
            self.victoire.draw()
        elif self.gm.get_affiche():
            self.gm.draw()
        elif self.chosemaps.get_affiche():
            self.chosemaps.draw()
        else:
            pyxel.blt(0, 0, 1, 0, 0, 256, 256)
            self.colision.draw()
            self.voiture.draw()
            self.in_game.draw()
            if self.debug_menu:
                self.tour.draw()
                self.voiture.debug()

App()