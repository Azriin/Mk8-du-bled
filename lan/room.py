import pyxel
from menus.menu import Menu
import addon_pyxel
import constante as c
import engine.visuMap as visuMap
import lan.renameRoom as renameRoom
import lan.tchat as tchat
import constante as c
import time

class MenuLan(Menu):
    def __init__(self, nom, actif, client):
        super().__init__(nom, actif)
        self.nbr_joueur = 1
        self.ready = [addon_pyxel.Bouton_radio(81, 34+45*i, False, 16, col_over=6) for i in range(4)]
        self.client = client
        self.carte = c.carte
        self.tour = c.max_lape
        self.bouton = {
            "menu": (addon_pyxel.Bouton_slide(45, 219, "menu", speed=-5, max_x=-25), self.set_menu),
            "play": (addon_pyxel.Bouton_slide(130, 219, "play"), self.set_play)
        }
        self.radtour = {1 : addon_pyxel.Bouton_radio(212, 135, False, 16),
                        3 : addon_pyxel.Bouton_radio(212, 158, True, 16),
                        5 : addon_pyxel.Bouton_radio(212, 181, False, 16)}
        self.texts = {
            ":1": addon_pyxel.BigTexte(232, 136, ":1"),
            ":3": addon_pyxel.BigTexte(232, 159, ":3"),
            ":5": addon_pyxel.BigTexte(232, 182, ":5"),
            "roomName": addon_pyxel.BigTexte(3, 1, self.client.getName())
        }
        self.visu = visuMap.Visu(self.carte, 16/3)
        self.load = renameRoom.RenameRoom(False, self.client)
        self.tchat = tchat.tchat(client)
        self.playable = True

    def set_menu(self):
        super().reverse_actif()
        self.client.nodeShutDown()
        self.set_nom("choseLan")

    def set_play(self):
        if self.ready[self.client.getID()].actif:
            if self.client.admin and self.client.getAllReady():
                self.client.sendMessage("InGame", f"StartRace {c.nbr_lan_player} {c.max_lape} {time.time()+c.ARRET} {c.carte}")
            else:
                self.client.sendMessage("Text", "I want to play")
        else:
            self.ready[self.client.getID()].reverse()
            self.client.sendMessage("System", f"AddReady {self.client.getID()} {self.ready[self.client.getID()].actif}")
            if self.ready[self.client.getID()].actif:
                message = "I am ready !"
            else:
                message = "I am no longer ready..."
            self.client.sendMessage("Text", message)

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
        for i in range(self.nbr_joueur):
            if self.client.getID() == i:
                pyxel.blt(9, 35+i*45, 0, 216+10*i, 116, 10, 15, 4)
            else : pyxel.blt(9, 35+i*45, 0, 216+10*i, 56, 10, 15, 4) #numéro
            pyxel.blt(27, 36+45*i, 0, 219, 243, 4, 12, 4)#: entre num et tuture
            pyxel.blt(63, 36+45*i, 0, 219, 243, 4, 12, 4)#: entre tuture et controle
            pyxel.blt(39, 36+45*i, 0, 16*i, 41, 16, 12, 4)#voiture
            pyxel.blt(1, 63+45*i, 0, 0, 87, 112, 3, 4)#barre
            try:
                self.ready[i].draw()
            except: pass
        pyxel.rectb(140, 148, 48, 48, 13)
        self.visu.draw(141, 149)
        #code
        self.tchat.draw()
        if self.client.admin:
            pyxel.blt(96, 1, 0, 16, 53, 16, 16, 4)
            self.load.draw()
        
    def update(self):
        if c.max_lape != self.tour:
            self.tour = c.max_lape
        if c.nbr_lan_player != self.nbr_joueur:
            self.nbr_joueur = c.nbr_lan_player
        if c.carte != self.carte:
            self.carte = c.carte
        if self.load.get_actif():
            self.load.update()
            self.texts["roomName"].setText(self.client.getName())
        else:
            for cle in self.bouton:
                self.bouton[cle][0].animation()
                if self.bouton[cle][0].clic():
                    self.bouton[cle][1]()
            #tour
            for cle in self.radtour:
                self.radtour[cle].actif = self.tour == cle
                self.radtour[cle].animation()
                if self.radtour[cle].clic():
                    if self.client.admin:
                        self.tour = cle
                        self.client.sendMessage("System", f"MaxLape {cle}")
                    else: self.client.sendMessage("Text", f"I want a {cle} lapes race")
            #map
            if self.visu.get_map() != c.carte:
                self.visu.set_map(c.carte)
            #name
            self.tchat.update()
            self.texts["roomName"].setText(self.client.getName())
            if self.client.admin and 96 <= pyxel.mouse_x <= 111 and 1 <= pyxel.mouse_y <= 16:
                if self.playable:
                    pyxel.play(0, 1)
                    self.playable = False
                pyxel.rectb(96, 1, 16, 16, 10)
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    pyxel.play(0, 0)
                    self.load.actif = True
            elif 140 <= pyxel.mouse_x <= 188 and 148 <= pyxel.mouse_y <= 195:
                if self.playable:
                    pyxel.play(0, 1)
                    self.playable = False
                pyxel.rectb(140, 148, 48, 48, 10)
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    pyxel.play(0, 0)
                    super().reverse_actif()
                    super().set_nom("selecteur_map")
            else: self.playable = True
            #ready
            self.ready[self.client.getID()].animation()
            if self.ready[self.client.getID()].clic():
                self.ready[self.client.getID()].reverse()
                self.client.sendMessage("System", f"AddReady {self.client.getID()} {self.ready[self.client.getID()].actif}")
                if self.ready[self.client.getID()].actif:
                    message = "I am ready !"
                else:
                    message = "I am no longer ready..."
                self.client.sendMessage("Text", message)

            try:
                for i in range(len(self.ready)):
                    if self.client.lstready[i] != self.ready[i].actif:
                        self.ready[i].reverse()
            except: pass