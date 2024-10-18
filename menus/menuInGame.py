import pyxel
import addon_pyxel
import constante as c
import voitures
import loadMap
import menus.menu as menu

class In_game(menu.Menu):
    def __init__(self, nom, actif):
        super().__init__(nom, actif)
        self.debug_menu = False
        self.map = loadMap.Load(c.carte)
        self.timer = pyxel.frame_count
        self.arret = c.arret
        self.textTimer = addon_pyxel.BigTexte(123, 118, str(self.arret))
        self.players = voitures.Lst_Cars(c.nbr_player, self.map.get_starts())
        self.triPlayers = self.players.get_cars()[:]

    def drawTimer(self):
        if self.timer + self.arret*c.frame_rate > pyxel.frame_count:
            self.textTimer.draw()
            if pyxel.frame_count%30 == 0:
                self.textTimer.setText(str(int(self.textTimer.getText())-1))
                pyxel.play(0, 2)


    def get_players(self):
        return self.triPlayers
    
    def restart(self):
        self.map = loadMap.Load(c.carte)
        self.timer = pyxel.frame_count
        self.textTimer = addon_pyxel.BigTexte(123, 118, str(self.arret))
        self.players = voitures.Lst_Cars(c.nbr_player, self.map.get_starts())
        self.triPlayers = self.players.get_cars()[:]

    def verif_lape(self):
        for tuture in self.players.get_cars():
            if tuture.get_lape() == c.max_lape:
                return True
        return False

    def draw(self):
        pyxel.mouse(False)
        pyxel.cls(11)
        self.map.draw()
        self.players.draw()
        if self.debug_menu:
            self.map.drawDebug()
            self.players.debug()

        self.drawTimer()        
        
        for i in range(len(self.triPlayers)):
            pyxel.blt(11 + 61*i, 239, 0, 216+10*i, 56, 10, 15, 4)#position
            pyxel.blt(23 + 61*i, 240, 0, 219, 243, 4, 12, 4)#:
            self.triPlayers[i].draw_win(29+61*i, 240)#voiture
            pyxel.blt(47 + 61*i, 240, 0, 219, 243, 4, 12, 4)#:
            addon_pyxel.BigTexte(53 + 61 * i, 239, str(self.triPlayers[i].get_lape())).draw()
            if len(self.triPlayers) - 1 != i:
                pyxel.blt(66 + 61*i, 238, 0, 253, 38, 3, 17, 4)#separateur

    def update(self):
        self.triPlayers = menu.tri_insertion(self.triPlayers)
        self.players.update(self.map.get_bordure(), self.map.get_separateur())
        if self.timer + self.arret*30 < pyxel.frame_count:
            for car in self.players.get_cars():
                car.reverse_brake(False)
        else:
            for car in self.players.get_cars():
                car.reverse_brake(True)

        if self.verif_lape():
            super().set_nom("victoire")
            super().reverse_actif()
        if pyxel.btnp(pyxel.KEY_BACKSPACE):
            super().set_nom("gamemode")
            super().reverse_actif()
        if pyxel.btnp(pyxel.KEY_B):
                self.debug_menu = not(self.debug_menu)
        if self.debug_menu:
            self.players.switch_debug_car()
            
