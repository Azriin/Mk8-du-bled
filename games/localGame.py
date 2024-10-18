import games.game as game
import menus.menuChoseMaps as ChoseMaps
import menus.menuGameMode as GameMode
import menus.menuInGame as InGame
import menus.menuVictoire as Victoire

class LocalGame(game.Game):
    def __init__(self, nom, actif):
        super().__init__(nom, actif)
        self.menus["gamemode"] = GameMode.GameMode("gamemode", True)
        self.menus["victoire"] = Victoire.Victoire("victoire", False)
        self.menus["en_jeu"] = InGame.In_game("en_jeu", False)
        self.menus["selecteur_map"] = ChoseMaps.ChoseMaps("selecteur_map", False)


    def update(self):
        super().update()
        for cle in self.menus:
            if self.menus[cle].get_nom() == "principale":
                self.menus[cle].set_nom(cle)
                self.menus["gamemode"].reverse_actif()
                self.set_nom("principale")
                self.reverse_actif()
            elif self.menus[cle].get_nom() != cle:
                self.menus[self.menus[cle].get_nom()].reverse_actif()
                self.menus[cle].set_nom(cle)
                self.menus["victoire"].actu_players(self.menus["en_jeu"].get_players())
                self.menus["en_jeu"].restart()
                self.menus["selecteur_map"].reload()