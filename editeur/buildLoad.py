import addon_pyxel as ap
import pyxel
import os

class LoadMenu:
    def __init__(self, actif):
        self.actif = actif
        dossier = "./maps/"
        self.lstCartes = [f[:-4] for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))]
        self.page = 0
        self.selection = -1
        self.text = ap.BigTexte(43, 87, "load map:")
        self.back = ap.TextButton(157, 85, "back", 0, 1)

    def update(self):
        if self.actif:
            self.page += pyxel.mouse_wheel if 12*self.page > len(self.lstCartes) else 0
            self.page = 0 if self.page < 0 else self.page

            self.back.animation()
            if self.back.clic() or self.selection != -1:
                self.reset()
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                for lig in range(4):
                    for col in range(3):
                        if 45+59*col <= pyxel.mouse_x <= 96+59*col and 110+14*lig <= pyxel.mouse_y <= 122+14*lig and len(self.lstCartes) > 12*self.page+3*lig+col:
                            self.selection = 12*self.page+3*lig+col
                
                
    def draw(self):
        if self.actif:
            pyxel.rect(36, 81, 184, 94, 1)
            pyxel.rect(37, 81, 183, 93, 7)
            pyxel.rect(38, 82, 181, 91, 5)
            self.text.draw()
            self.back.draw()
            for lig in range(4):
                for col in range(3):
                    if len(self.lstCartes) > 12*self.page+3*lig+col:
                        if 45+59*col <= pyxel.mouse_x <= 96+59*col and 110+14*lig <= pyxel.mouse_y <= 122+14*lig:
                            pyxel.rect(45+59*col, 110+14*lig, 52, 13, 1)
                            pyxel.pset(45+59*col, 110+14*lig, 5)
                            pyxel.pset(45+59*col, 122+14*lig, 5)
                            pyxel.pset(96+59*col, 110+14*lig, 5)
                            pyxel.pset(96+59*col, 122+14*lig, 5)
                        pyxel.text(50+59*col, 114+14*lig, self.lstCartes[12*self.page+3*lig+col], 7)

    def getActif(self):
        return self.actif
    
    def set_actif(self, val):
        self.actif = val

    def getSelection(self):
        return self.selection
    
    def getCarte(self, i):
        return self.lstCartes[i]

    def reset(self):
        self.selection = -1
        self.actif = False