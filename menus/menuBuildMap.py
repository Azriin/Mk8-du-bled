import pyxel
import editeur.buildSquare as sb
import editeur.buildGUI as tool
import editeur.buildCircle as cb
import editeur.buildDist as db
import editeur.buildStart as stb
import editeur.buildSave as sm
import editeur.buildLoad as bl
import loadMap as lm
import editeur.buildDeco as bd
import editeur.buildNew as bn
from menus.menu import Menu

class Editor(Menu):
    def __init__(self, nom, actif):
        super().__init__(nom, actif)
        self.tool = {
            "road": cb.roadBuilder(),
            "wall": sb.CreationMurs(),
            "separator": sb.CreationSep(),
            "dist_next": db.CreationPoint(),
            "starts": stb.CreationStart(),
            "deco": bd.MenuDeco()
        }
        self.menuAction = {
            "save": self.set_save,
            "quit": self.set_quit,
            "load": self.set_load,
            "new": self.set_new
        }
        self.menu = {
            "save": sm.SaveMenu(False, self.tool),
            "load": bl.LoadMenu(False),
            "new": bn.MenuNew(False)
        }
        self.guiTool = tool.GUITool()
        self.cross = False
        self.debug = False
        self.cle = ["road", "wall", "separator", "dist_next", "starts", "deco"]
        self.indice = 0

    def draw(self):
        pyxel.cls(11)
        for key in self.tool:
            self.tool[key].draw()
            if self.debug:
                pyxel.text(3, 3, f"{self.cle[self.indice]}:", 0)
                self.tool[self.cle[self.indice]].draw_debug()
        if self.cross:
            pyxel.line(0, pyxel.mouse_y, 256, pyxel.mouse_y, 0)
            pyxel.line(pyxel.mouse_x, 0, pyxel.mouse_x, 256, 0)
        self.guiTool.draw()
        for key in self.menu:
            self.menu[key].draw()

    def update(self):
        if pyxel.btnp(pyxel.KEY_B):
            self.debug = not(self.debug)
        for i in range(len(self.cle)):
            if eval(f"pyxel.btn(pyxel.KEY_{i+1})"):
                self.indice = i
        if pyxel.btnp(pyxel.KEY_CTRL):
            self.cross = not(self.cross)
        if self.guiTool.get_boutSelect() != None:
            self.menuAction[self.guiTool.get_boutSelect()]()
        elif self.menu["save"].getActif():
            self.menuAction["save"]()
        elif self.menu["load"].getActif():
            self.menuAction["load"]()
        elif self.menu["new"].getActif():
            self.menuAction["new"]()
        else:
            if not(self.guiTool.get_actif()) and self.guiTool.get_key() != None:
                if self.guiTool.get_key() == "dist_next":
                    self.tool[self.guiTool.get_key()].update(self.tool["separator"].getLst())
                elif self.guiTool.get_key() == "separator":
                    self.tool[self.guiTool.get_key()].update(self.tool["dist_next"].lstPoint)
                else: self.tool[self.guiTool.get_key()].update()
            self.guiTool.update()

    def set_save(self):
        if not self.menu["save"].getActif():
            self.menu["save"].actu_dico(self.tool)
            self.menu["save"].set_actif(True)
            self.guiTool.reset()
        self.menu["save"].update()

    def set_quit(self):
        self.guiTool.quit = False
        super().reverse_actif()
        super().set_nom("principale")
        self.guiTool.reset()


    def set_new(self):
        if not self.menu["new"].getActif():
            self.menu["new"].set_actif(True)
            self.guiTool.reset()
        self.menu["new"].update()
        if self.menu["new"].newMap:
            self.tool = {
                "road": cb.roadBuilder(),
                "wall": sb.CreationMurs(),
                "separator": sb.CreationSep(),
                "dist_next": db.CreationPoint(),
                "starts": stb.CreationStart(),
                "deco": bd.MenuDeco()
            }
            self.menu["new"].newMap = False


    def set_load(self):
        if not self.menu["load"].getActif():
            self.menu["load"].set_actif(True)
            self.guiTool.reset()
        self.menu["load"].update()
        if self.menu["load"].getSelection() != -1:
            carte = lm.Load(self.menu["load"].getCarte(self.menu["load"].getSelection())+".txt")
            self.tool["road"].loadRoad(carte.get_route())
            self.tool["wall"].loadMurs(carte.get_bordure())
            self.tool["separator"].loadSep(carte.get_separateur())
            self.tool["dist_next"].loadDist(carte.get_separateur())
            self.tool["starts"].loadStart(carte.get_starts())
            self.tool["deco"].loadDeco(carte.get_deco())
    
            self.menu["load"].reset()
            