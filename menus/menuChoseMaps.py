import pyxel
import os
import addon_pyxel
import visuMap
import constante as c
from menus.menu import Menu

class ChoseMaps(Menu):
    def __init__(self, nom, actif, client=None):
        super().__init__(nom, actif)
        self.selection = c.carte
        self.page = 0
        dossier = "./maps/"
        self.lstCarte = [f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))]
        self.bouton = {"menu": addon_pyxel.Bouton_slide(129, 218, "menu")}
        self.lstVisus = [visuMap.Visu(self.lstCarte[i], 16/3) for i in range(len(self.lstCarte))]
        self.client = client
        self.boutonAction = {"menu": self.set_gamemode}
        if len(self.lstCarte) > 6:
            self.bouton["next"] = addon_pyxel.Bouton_slide(111, 187, "next")
            self.boutonAction["next"] = self.next_page

        # self.playable = True

    def set_gamemode(self):
        super().set_nom("gamemode")
        super().reverse_actif()

    def next_page(self):
        self.page += 1
        if 6*self.page > len(self.lstCarte):
            self.page = 0

    def reload(self):
        dossier = "./maps/"
        debug = [f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))]
        for i in range(len(debug)):
            if debug[i] not in self.lstCarte:
                self.lstCarte.append(debug[i])
            if debug[i] not in self.lstVisus:
                self.lstVisus.append(visuMap.Visu(debug[i], 16/3))
        if len(self.lstCarte) > 6:
            self.bouton["next"] = addon_pyxel.Bouton_slide(111, 187, "next")
            self.boutonAction["next"] = self.next_page

    def update(self):
        if pyxel.btnp(pyxel.KEY_R):
            self.reload()
        if c.carte != self.selection:
            if not(self.client):
                c.carte = self.selection
            if self.client and self.client.admin:
                c.carte = self.selection
                self.client.sendMessage("System", f"MapChange {c.carte}", self.client.port)        
        
        for cle in self.bouton:
            self.bouton[cle].animation()
            if self.bouton[cle].clic():
                self.boutonAction[cle]()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            lig, col = -1, -1 
            if 31 <= pyxel.mouse_y <= 89:
                lig = 0
            elif 111 <= pyxel.mouse_y <= 169:
                lig = 1

            if 23 <= pyxel.mouse_x <= 72:
                col = 0
            elif 103 <= pyxel.mouse_x <= 152:
                col = 1
            elif 183 <= pyxel.mouse_x <= 232:
                col = 2

            if lig >= 0 and col >= 0 and 6*self.page+3*lig+col < len(self.lstCarte):
                pyxel.play(0, 0)
                if self.client and not(self.client.admin):
                    carte = self.lstCarte[6*self.page+3*lig+col][:-4]
                    self.client.sendMessage("Text", f"I want to play on {carte}", self.client.port)
                else: 
                    self.selection = self.lstCarte[6*self.page+3*lig+col]
        
    def draw(self):
        pyxel.mouse(True)
        pyxel.tri(77, 0, 77, 255, 224, 255, 6)
        pyxel.rect(0, 0, 77, 255, 6)
        for cle in self.bouton:
            self.bouton[cle].draw()
        for i in range(2):
            for j in range(3):
                if 6*self.page+3*i+j < len(self.lstCarte):
                    self.lstVisus[6*self.page+3*i+j].draw(25+81*j, 33+81*i)
                    pyxel.text(24+81*j, 84+81*i, self.lstCarte[6*self.page+3*i+j], 0)
                    col = 13
                    if self.selection == self.lstCarte[6*self.page+3*i+j]:
                        col = 10
                        pyxel.rectb(23+81*j, 31+81*i, 50, 50, col)
                    pyxel.rectb(24+81*j, 32+81*i, 48, 48, col)


