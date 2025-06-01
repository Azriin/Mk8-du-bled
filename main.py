import pyxel
import menus.menuPrincipal as Principal
import menus.menuBuildMap as buildMap
import games.localGame as localGame
import games.lanGame as lanGame
import constante as c

class App:
    def __init__(self):
        pyxel.init(256, 256, "Mk8 du bled", fps=c.FRAME_RATE)
        pyxel.image(0).load(0, 0, "images/images.png")
        pyxel.sound(0).set("g4c4", "s", "3", "f", 7)#interacion
        pyxel.sound(1).set("e4", "p", "1", "n", 5)#mouse over
        pyxel.sound(2).set("c2", "t", "3", "n", 10)#start light timer
        pyxel.sound(3).set("a3d#3", "s", "1", "f", 7)#reception msg
        pyxel.sound(4).set("c2", "n", "1", "f", 10)#bruit tutures
        pyxel.sound(5).set("c4e4g4a4", "p", "2", "f", 20)#bruit de victoire
        self.menus = {
            "principale": Principal.MenuPrincipal("principale", True),
            "edit": buildMap.Editor("edit", False),
            "local": localGame.LocalGame("local", False),
            "lan": lanGame.LanGame("lan", False)
        }
        pyxel.run(self.draw, self.update)
        
    def update(self):
        for cle in self.menus:
            if self.menus[cle].get_actif():
                self.menus[cle].update()
            if self.menus[cle].get_nom() != cle:
                self.menus[self.menus[cle].get_nom()].reverse_actif()
                self.menus[cle].set_nom(cle)
 
    def draw(self):
        pyxel.cls(7)
        for cle in self.menus:
            if self.menus[cle].get_actif():
                self.menus[cle].draw()

if __name__ == "__main__":
    app = App()