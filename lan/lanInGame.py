import menus.menuInGame as InGames
import menus.menu as menu
import constante as c
import pyxel
import time

class LanInGame(InGames.In_game):
    def __init__(self, nom, actif, client):
        super().__init__(nom, actif)
        self.client = client
        self.temp = None

    def drawTimer(self):
        if self.client.timeStart > time.time():
            oldTimer = self.textTimer.getText()
            self.textTimer.setText(str(int(self.client.timeStart - time.time())+1))
            if oldTimer != self.textTimer.getText():
                pyxel.play(0, 2)
            self.textTimer.draw()

    def verifCarLape(self, carId):
         return self.players.get_cars()[carId].get_lape() == c.max_lape

    def update(self):
        carInfo = self.players.get_cars()[self.client.id]
        self.players.update(self.map.get_bordure(), self.map.get_separateur())
        if self.client.timeStart < time.time():
            carInfo.reverse_brake(False)
            self.triPlayers = menu.tri_insertion(self.triPlayers)
            self.client.sendMessage("InGame", f"CarMove {self.client.id} {carInfo.x} {carInfo.y} {carInfo.degre}")
        else: 
            carInfo.reverse_brake(True)
            self.client.sendMessage("InGame", f"StartRace {c.nbr_lan_player} {c.max_lape} {self.client.timeStart} {c.carte}")

        if self.verifCarLape(self.client.id):
             if not(self.temp):
                self.temp = time.time()
             self.client.sendMessage("InGame", f"CarFinish {self.client.id} {self.temp}")
             carInfo.reverse_brake(True)
        if len(self.client.lstFinish) == max(c.nbr_player-1, 1):
            self.client.sendMessage("InGame", "SwitchWin")

        
        msgUpdateCar = self.client.getCarMovement()
        for movement in msgUpdateCar:
            carInfo = self.players.get_cars()[movement[0]]
            carInfo.x = movement[1]
            carInfo.y = movement[2]
            carInfo.degre = movement[3]


        if pyxel.btnp(pyxel.KEY_B):
                self.players.nbr_debug_car = self.client.id
                self.debug_menu = not(self.debug_menu)