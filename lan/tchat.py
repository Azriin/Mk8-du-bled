import pyxel
import addon_pyxel

class tchat:
    def __init__(self, client):
        self.client = client
        self.historique = []
        self.entry = addon_pyxel.Entry(122, 116, 30, littleTxt=True)
        self.maxHistorique = 10
        self.couleur = [0, 1, 8, 3, 5]

    def addMsg(self, message, origine):
        self.historique.append((message, int(origine)))

    def draw(self):
        pyxel.rect(118, 0, 2, 129, 0)
        pyxel.rect(119, 128, 137, 2, 0)
        pyxel.rect(120, 113, 136, 15, 13)
        for i in range(len(self.historique)):
            pyxel.text(123, 5+10*i, self.historique[i][0], self.couleur[self.historique[i][1]])
        self.entry.draw()


    def update(self):
        self.entry.update()
        messages = self.client.get_historique()
        if messages:
            for message in messages:
                self.addMsg(message[1], message[0])
                pyxel.play(1,3)
                if len(self.historique) > self.maxHistorique:
                    self.historique.pop(0)
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.client.sendMessage("Text", self.entry.getText(), self.client.port)
            self.entry.text = ""