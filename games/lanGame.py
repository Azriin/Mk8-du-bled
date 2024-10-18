import games.game as game
import menus.menuChoseMaps as ChoseMaps
import lan.lanVictoire as Victoire
import lan.room as room
import lan.choseRoom as choseRoom
import lan.lanInGame as InGame
import lan.nodeUDP as nodeUDP


class LanGame(game.Game):
    def __init__(self, nom, actif):
        super().__init__(nom, actif)
        self.clt = nodeUDP.NoeudUDP()
        self.menus["choseLan"] = choseRoom.MenuChoseLan("choseLan", True, self.clt)
        self.menus["gamemode"] = room.MenuLan("gamemode", False, self.clt)
        self.menus["selecteur_map"] = ChoseMaps.ChoseMaps("selecteur_map", False, self.clt)
        self.menus["en_jeu"] = InGame.LanInGame("en_jeu", False, self.clt)
        self.menus["victoire"] = Victoire.LanVictoire("victoire", False)


    def update(self):
        super().update()
        for cle in self.menus:
            if self.menus[cle].get_nom() == "principale":
                self.menus[cle].set_nom(cle)
                self.menus["choseLan"].reverse_actif()
                self.set_nom("principale")
                self.reverse_actif()
                self.clt.nodeShutDown()
            elif self.menus[cle].get_nom() != cle:
                self.menus[self.menus[cle].get_nom()].reverse_actif()
                self.menus[cle].set_nom(cle)
                self.menus["selecteur_map"].reload()
                self.menus["en_jeu"].restart()

        if self.actif and not(self.clt.isRunning):
            self.clt.startConnection()
        
        if self.clt.inGame and self.menus["gamemode"].get_actif():
            self.menus["gamemode"].reverse_actif()
            self.menus["en_jeu"].reverse_actif()
            self.menus["en_jeu"].restart()

        if self.clt.inWin and self.menus["en_jeu"].get_actif():
            self.menus["victoire"].reverse_actif()
            self.menus["en_jeu"].reverse_actif()
            self.menus["victoire"].actu_players(self.clt.lstFinish)