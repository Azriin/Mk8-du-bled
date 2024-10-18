import menus.menu as menu

class Game(menu.Menu):
    def __init__(self, nom, actif):
        super().__init__(nom, actif)
        self.menus = {}

    def draw(self):
        if self.get_actif():
            for key in self.menus:
                if self.menus[key].get_actif():
                    self.menus[key].draw()

    def update(self):
        if self.get_actif():
            for cle in self.menus:
                if self.menus[cle].get_actif():
                    self.menus[cle].update()