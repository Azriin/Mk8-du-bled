import menus.menu as menu
import addon_pyxel
import lan.getIpv4 as ip
import pyxel
import constante as c

class MenuChoseLan(menu.Menu):
    def __init__(self, nom, actif, clt):
        super().__init__(nom, actif)
        self.clt = clt
        self.bouton = {
            "back": (addon_pyxel.Bouton_slide(32, 217, "menu", -5, -25), self.get_back),
            "create": (addon_pyxel.TextButton(167, 8, "create", 6, 12), self.get_create),
            "next": (addon_pyxel.Bouton_slide(143, 217, "next"), self.next_page)
        }
        self.texts = [
            addon_pyxel.BigTexte(11, 11, "ROOM LIST:"),
            addon_pyxel.BigTexte(22, 56, "name:"),
            addon_pyxel.BigTexte(115, 56, "players")
        ]
        self.butConnectRoom = []
        self.page = 0
        self.maxRoom = 4

    def draw(self):
        pyxel.mouse(True)
        #fond
        pyxel.tri(77, 0, 77, 255, 224, 255, 6)
        pyxel.rect(0, 0, 77, 256, 6)
        pyxel.rectb(4, 47, 248, 154, 1)
        pyxel.rectb(5, 47, 189, 153, 7)
        pyxel.rectb(194, 47, 58, 153, 6)
        pyxel.line(104, 47, 194, 47, 6)
        pyxel.rect(6, 48, 245, 151, 5)
        #bouttons
        for cle in self.bouton:
            self.bouton[cle][0].draw()
        for txt in self.texts:
            txt.draw()
        pyxel.blt(8, 28, 0, 0, 87, 112, 3, 4)

        for i in range(self.maxRoom):
            if self.maxRoom*self.page+i < len(self.clt.getLstRoom()):
                pyxel.blt(128, 77+31*i, 0, 1, 87, 111, 3, 4)
                pyxel.blt(17, 77+31*i, 0, 0, 87, 111, 3, 4)
                addon_pyxel.BigTexte(22, 86+31*i, self.clt.getLstRoom()[self.maxRoom*self.page+i][2]+':').draw()
                addon_pyxel.BigTexte(137, 86+31*i, f"{self.clt.getLstRoom()[self.maxRoom*self.page+i][1]}-{c.max_player}").draw()
                try:
                    if int(self.clt.getLstRoom()[self.maxRoom*self.page+i][1]) < c.max_player:
                        self.butConnectRoom[self.maxRoom*self.page+i].draw()
                except: pass




    def update(self):
        if len(self.clt.getLstRoom()) != len(self.butConnectRoom):
            i = len(self.butConnectRoom)
            col_in = 6 if i%2 == 0 else 7
            col_out = 6 if col_in == 7 else 7
            if len(self.clt.getLstRoom()) > len(self.butConnectRoom):
                self.butConnectRoom.append(addon_pyxel.TextButton(179, 82+31*(i%self.maxRoom), "join", col_in, col_out))
            else: self.butConnectRoom.pop()
        for cle in self.bouton:
            self.bouton[cle][0].animation()
            if self.bouton[cle][0].clic():
                
                self.bouton[cle][1]()
        for i in range(len(self.butConnectRoom)):
            self.butConnectRoom[i].animation()
            if int(self.clt.getLstRoom()[i][1]) < c.max_player and self.butConnectRoom[i].clic():
                self.get_coonect(self.clt.getLstRoom()[i][0])

    def get_back(self):
        super().reverse_actif()
        self.set_nom("principale")

    def get_create(self):
        super().reverse_actif()
        self.clt.connectNewPort(True, c.init_Port+int(ip.get_code_room()))
        self.set_nom("gamemode")

    def get_coonect(self, code):
        super().reverse_actif()
        self.clt.connectNewPort(False, code)
        self.set_nom("gamemode")

    def next_page(self):
        self.page += 1
        if self.maxRoom*self.page > len(self.clt.getLstRoom()):
            self.page = 0
            