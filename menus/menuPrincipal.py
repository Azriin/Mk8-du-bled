import pyxel
from menus.menu import Menu
import addon_pyxel
import constante

class MenuPrincipal(Menu):
    def __init__(self, nom, actif):
        super().__init__(nom, actif)
        self.bouton = {
            "local": (addon_pyxel.Bouton_slide(53, 86, "local"), self.set_local),
            "leave": (addon_pyxel.Bouton_slide(131, 221, "leave"), self.quit),
            "edit": (addon_pyxel.Bouton_slide(97, 162, "edit"), self.set_edit),
            "lan": (addon_pyxel.Bouton_slide(75, 124, "lan"), self.set_lan)
        }

    def set_local(self):
        self.set_nom("local")

    def quit(self):
        pyxel.quit()

    def set_edit(self):
        self.set_nom("edit")
        
    def set_lan(self):
        self.set_nom("lan")

    def draw(self):
        pyxel.mouse(True)
        pyxel.tri(77, 0, 77, 255, 224, 255, 6)
        pyxel.rect(0, 0, 77, 256, 6)
        pyxel.blt(125, 17, 0, 0, 90, 128, 38, 13)
        pyxel.text(5, 247, constante.VERSION, 0)
        for cle in self.bouton:
            self.bouton[cle][0].draw()

    def update(self):
        for cle in self.bouton:
            self.bouton[cle][0].animation()
            if self.bouton[cle][0].clic():
                super().reverse_actif()
                self.bouton[cle][1]()
