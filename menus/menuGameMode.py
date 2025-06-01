import pyxel
from menus.menu import Menu
import addon_pyxel
import constante as c
import visuMap

class GameMode(Menu):
    def __init__(self, nom, actif):
        super().__init__(nom, actif)
        self.nbr_joueur = c.nbr_player
        self.tour = c.max_lape
        self.bouton = {
            "jouer": (addon_pyxel.Bouton_slide(130, 219, "play"), self.set_en_jeu,),
            "menu": (addon_pyxel.Bouton_slide(145, 4, "menu"), self.set_principale)
        }
        self.radtour = {1 : addon_pyxel.Bouton_radio(196, 71, False, 16),
                        3 : addon_pyxel.Bouton_radio(196, 94, True, 16),
                        5 : addon_pyxel.Bouton_radio(196, 117, False, 16)}
        self.poussoir = {
            "add": addon_pyxel.bouton_poussoir(13, 27, 0, 11),
            "rem": addon_pyxel.bouton_poussoir(86, 27, 1, 8)
        }
        self.texts = {
            "joueur:": addon_pyxel.BigTexte(3, 1, "players:"),
            "tour:": addon_pyxel.BigTexte(192, 50, "lape:"),
            ":1": addon_pyxel.BigTexte(218, 72, ":1"),
            ":3": addon_pyxel.BigTexte(218, 95, ":3"),
            ":5": addon_pyxel.BigTexte(218, 118, ":5"),
            "carte": addon_pyxel.BigTexte(192, 194, "maps")
        }
        self.visu = visuMap.Visu(c.carte, 16/3)
        self.playable = True


    def set_en_jeu(self):
        super().set_nom("en_jeu")

    def set_principale(self):
        super().set_nom("principale")

    def draw(self):
        pyxel.mouse(True)
        #fond
        pyxel.tri(78, 0, 225, 255, 225, 0, 6)
        pyxel.rect(226, 0, 30, 256, 6)
        #bouttons
        for cle in self.bouton:
            self.bouton[cle][0].draw()
        for cle in self.texts:
            self.texts[cle].draw()
        for cle in self.radtour:
            self.radtour[cle].draw()
        pyxel.blt(1, 18, 0, 0, 87, 112, 3, 4)
        if self.nbr_joueur != c.MAX_PLAYER:
            self.poussoir["add"].draw()
        if self.nbr_joueur != c.MIN_PLAYER:
            self.poussoir["rem"].draw()
        for i in range(self.nbr_joueur):
            pyxel.blt(9, 35+i*45, 0, 216+10*i, 56, 10, 15, 4) #numéro
            pyxel.blt(27, 36+45*i, 0, 219, 243, 4, 12, 4)#: entre num et tuture
            pyxel.blt(63, 36+45*i, 0, 219, 243, 4, 12, 4)#: entre tuture et controle
            pyxel.blt(39, 36+45*i, 0, 16*i, 41, 16, 12, 4)#voiture
            pyxel.blt(76, 26+45*i, 0, 32*i, 128, 32, 32, 4)#controle
            pyxel.blt(1, 63+45*i, 0, 0, 87, 112, 3, 4)#barre
        pyxel.rectb(195, 144, 48, 48, 13)
        self.visu.draw(196, 145)

    def update(self):
        #jouer
        for cle in self.bouton:
            self.bouton[cle][0].animation()
            if self.bouton[cle][0].clic():
                super().reverse_actif()
                self.bouton[cle][1]()
        #tour
        for cle in self.radtour:
            self.radtour[cle].actif = self.tour == cle
            self.radtour[cle].animation()
            if self.radtour[cle].clic():
                self.tour = cle
        #joueur
        if self.nbr_joueur != c.MAX_PLAYER:
            self.poussoir["add"].animation()
            self.poussoir["add"].edit_y(27 + self.nbr_joueur*45)
            if self.poussoir["add"].clic():
                self.nbr_joueur += 1 if self.nbr_joueur < c.MAX_PLAYER else 0
        if self.nbr_joueur != c.MIN_PLAYER:
            self.poussoir["rem"].animation()
            self.poussoir["rem"].edit_y(27 + self.nbr_joueur*45)
            if self.poussoir["rem"].clic():
                self.nbr_joueur -= 1 if self.nbr_joueur > c.MIN_PLAYER else 0
        #map
        if self.visu.get_map() != c.carte:
            self.visu.set_map(c.carte)
        if 195 <= pyxel.mouse_x <= 243 and 144 <= pyxel.mouse_y <= 192:
            pyxel.rectb(195, 144, 48, 48, 10)
            if self.playable:
                pyxel.play(0, 1)
                self.playable = False
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                pyxel.play(0, 0)
                super().reverse_actif()
                super().set_nom("selecteur_map")
        else: self.playable = True
        #actu info
        if self.nbr_joueur != c.nbr_player:
            c.nbr_player = self.nbr_joueur
        if self.tour != c.max_lape:
            c.max_lape = self.tour