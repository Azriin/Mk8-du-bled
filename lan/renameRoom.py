import pyxel
import addon_pyxel
import lan.getIpv4 as ip

class RenameRoom:
    def __init__(self, actif, client):
        self.actif = actif
        self.client = client
        self.boutons = {
            "back": (addon_pyxel.TextButton(67, 140, "back", 0, 1), self.get_back),
            "changeName": (addon_pyxel.TextButton(130, 140, "okay", 12, 6), self.get_changeName)
        }
        self.texts = [
            addon_pyxel.BigTexte(68, 87, "rooms name:")
        ]
        self.entry = addon_pyxel.Entry(77, 107, 8, selection=True, text=f"room {ip.get_code_room()}")

    def get_actif(self):
        return self.actif

    def get_back(self):
        self.actif = False

    def get_changeName(self):
        self.client.sendMessage("Room", f"NameChange {self.entry.getText()}", self.client.port)
        self.actif = False

    def draw(self):
        if self.actif:
            pyxel.rectb(61, 81, 133, 94, 1)
            pyxel.rectb(62, 81, 62, 93, 6)
            pyxel.rectb(124, 81, 70, 93, 7)
            pyxel.line(124, 173, 177, 173, 6)
            pyxel.rect(63, 82, 130, 91, 5)
            for text in self.texts:
                text.draw()
            self.entry.draw()
            for key in self.boutons:
                self.boutons[key][0].draw()

    def update(self):
        if self.actif:
            self.entry.update()
            for key in self.boutons:
                self.boutons[key][0].animation()
                if self.boutons[key][0].clic():
                    self.boutons[key][1]()