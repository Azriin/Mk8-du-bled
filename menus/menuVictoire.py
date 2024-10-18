import pyxel
import menus.menu as menu
import addon_pyxel
import voitures
import loadMap
import constante as c

class Victoire(menu.Menu):
    def __init__(self, nom, actif, retour="gamemode"):
        super().__init__(nom, actif)
        self.players = voitures.Lst_Cars(1, loadMap.Load(c.carte).get_starts()).get_cars()
        self.titre = addon_pyxel.BigTexte(114, 20, "ranking:")
        self.back = addon_pyxel.Bouton_slide(115, 193, "menu")
        self.retour = retour
        self.soundPlayed = False

    def actu_players(self, new_players):
        self.players = new_players
        self.soundPlayed = False

    def classement(self):
        self.players = menu.tri_insertion(self.players)
        for i in range(len(self.players)):
            pyxel.blt(51, 85 + 24*i, 0, 216+10*i, 56, 10, 15, 4)#num
            pyxel.blt(70, 87 + 24*i, 0, 219, 243, 4, 12, 4)#:
            pyxel.blt(50, 103 + 24*i, 0, 0, 84, 50, 3, 4)#barre
            self.players[i].draw_win(83, 87+24*i)#tuture
        
    def draw(self):
        pyxel.mouse(True)
        #bg
        pyxel.tri(77, 0, 77, 255, 224, 255, 6)
        pyxel.rect(0, 0, 77, 255, 6)
        #objet
        self.titre.draw()
        pyxel.blt(138, 41, 0, 10, 113, 69, 9, 13)
        pyxel.blt(114, 37, 0, 0, 87, 112, 3, 4)
        self.back.draw()
        #classement
        self.classement()
        
    def update(self):
        if not(self.soundPlayed):
            pyxel.play(0, 5)
            self.soundPlayed = True
        self.back.animation()
        if self.back.clic():
            super().reverse_actif()
            super().set_nom(self.retour)