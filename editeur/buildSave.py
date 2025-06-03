import pyxel
import addon_pyxel as ap
import datetime

class SaveMenu:
    def __init__(self, actif, dicoTool):
        self.actif = actif
        self.dicoTool = dicoTool
        self.textSave1 = ap.BigTexte(43, 87, "Name of the new")
        self.textSave2 = ap.BigTexte(43, 111, "Map:")
        self.entre = ap.Entry(90, 107, 10, str(datetime.datetime.now().date()).replace('-', ''), col=6)
        self.back = ap.TextButton(59, 140, "Back", col_in=0, col_out=1)
        self.save = ap.TextButton(139, 140, "Save", col_in=12, col_out=6)

    def draw(self):
        if self.actif:
            pyxel.rect(36, 81, 184, 94, 1)
            pyxel.rect(37, 81, 183, 93, 7)
            pyxel.rect(38, 82, 181, 91, 5)
            self.textSave1.draw()
            self.textSave2.draw()
            self.entre.draw()
            self.back.draw()
            self.save.draw()

    def update(self):
        if self.actif:
            self.entre.update()
            self.back.animation()
            if self.back.clic():
                self.actif = False
            self.save.animation()
            if self.save.clic() and self.entre.getText() != "":
                Save(self.entre.getText(), **self.dicoTool)
                self.actif = False

    def actu_dico(self, newDico):
        self.dicoTool = newDico
    
    def set_actif(self, etat):
        self.actif = etat

    def getActif(self):
        return self.actif

class Save:
    def __init__(self, nom, road, wall, separator, dist_next, starts, deco, erase):
        with open("maps/"+nom+".txt", "w") as file:
            for r in road.get_road():
                file.write(f"{r.x, r.y, r.r, r.col}\n")
            file.write('\n')
            for w in wall.lstMurs:
                file.write(f"{w.x1, w.y1, w.x2-w.x1, w.y2-w.y1, w.col}\n")
            file.write('\n')
            if len(separator.lstSep) != len(dist_next.lstPoint) or len(separator.lstSep) == 0:
                file.write(f"""{0, 0, 256, 256, 0, (0, 0)}\n""")
            else:
                for i in range(len(separator.lstSep)):
                    idist = 0
                    while dist_next.lstPoint[idist].part != i:
                        idist += 1
                    file.write(f"""{separator.lstSep[i].x1, separator.lstSep[i].y1, separator.lstSep[i].x2-separator.lstSep[i].x1, 
                                separator.lstSep[i].y2-separator.lstSep[i].y1, i, (dist_next.lstPoint[idist].x, dist_next.lstPoint[idist].y)}\n""")
            file.write('\n')
            for start in starts.lstStart:
                file.write(f"{start.x, start.y, start.indice}\n")
            file.write('\n')
            for deco in deco.lstDeco:
                file.write(f"{deco.x, deco.y, deco.indice, deco.rotation}\n")
            file.write('\n')