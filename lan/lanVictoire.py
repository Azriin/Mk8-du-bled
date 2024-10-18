import menus.menuVictoire as menuVictoire
import constante as c
import voitures
import loadMap
import pyxel

def tri_matrice(matrice, numCol):
    for i in range(1, len(matrice)):
        v = matrice[i]
        j = i
        while j > 0 and matrice[j-1][numCol] > v[numCol]:
            matrice[j] = matrice[j-1]
            j -= 1
        matrice[j] = v
    return matrice


class LanVictoire(menuVictoire.Victoire):
    def __init__(self, nom, actif, retour="gamemode"):
        super().__init__(nom, actif, retour)
        self.modele = voitures.Lst_Cars(1, loadMap.Load(c.carte).get_starts()).get_cars()

    def actu_players(self, new_players):
        super().actu_players(new_players)
        self.modele = voitures.Lst_Cars(c.nbr_player, loadMap.Load(c.carte).get_starts()).get_cars()
        if len(self.players) != c.nbr_player:
            self.triPlayers()

    def triPlayers(self):
        self.players = tri_matrice(self.players, 1)
        lstId = [x for x in range(c.nbr_player)]
        for i in range(len(self.players)):
            if self.players[i][0] in lstId:
                lstId.remove(self.players[i][0])
        self.players.append((lstId[0], None))

    def classement(self):
        for i in range(len(self.players)):
            pyxel.blt(51, 85 + 24*i, 0, 216+10*i, 56, 10, 15, 4)#num
            pyxel.blt(70, 87 + 24*i, 0, 219, 243, 4, 12, 4)#:
            pyxel.blt(50, 103 + 24*i, 0, 0, 84, 50, 3, 4)#barre
            self.modele[self.players[i][0]].draw_win(83, 87+24*i)#tuture
