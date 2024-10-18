import socket
import threading
import lan.getIpv4 as ip
import constante as c
import time
LOCAL_ADDRESS = ip.get_ipv4_address()
GROUP_ADDRESS = "239.50.50.50"

class NoeudUDP:
#_____INIT/GET/RNT_____
    def __init__(self):
        self.commandRoom = {
            "NameChange": self.lanNameChange,
            "RoomInfo": self.lanRoomInfo,
            "DelRoom": self.lanDelRoom,
            "ActuConstanteLan": self.lanActuConstanteLan,
        }
        self.commandSystem = {
            "MaxLape": self.sysMaxLape,
            "AddPlayer": self.sysAddPlayer,
            "RemPlayer": self.sysRemPlayer,
            "MapChange": self.sysMapChange,
            "AddReady": self.sysAddReady,
        }
        self.commandInGame = {
            "StartRace": self.igStartRace,
            "CarMove": self.igCarMove,
            "CarFinish": self.igCarFinish,
            "SwitchWin": self.igSwitchWin,
        }

        self.compteurMsg = {
            "Room": [0, 0, 0, 0],
            "System": [0, 0, 0, 0],
            "InGame": [0, 0, 0, 0],
            "Text": [0, 0, 0, 0],
            "Time": [0, 0, 0, 0]
        }

        self.historique = []
        self.CarMovement = []
        self.lstRooms = []
        self.lstready = []
        self.lstFinish = []
        
        self.timeStart = 0
        self.delta = 5
        self.id = -1
        self.roomName = f"room {ip.get_code_room()}"
        self.isRunning = False
        self.admin = False
        self.inGame = False
        self.inRoom = False
        self.inWin = False

        self.port = c.init_Port
        self.sockBroadcast = None
        self.sockMessage = None

    def getID(self):
        return self.id
    
    def setName(self, nom):
        self.roomName = nom

    def getName(self):
        return self.roomName

    def getLstRoom(self):
        return self.lstRooms

    def get_historique(self):
        if len(self.historique) > 0:
            message = self.historique[:]
            self.historique = []        
            return message
        return None  
    
    def getCarMovement(self):
        return self.CarMovement

    def getAllReady(self):
        for bo in self.lstready:
            if not(bo):
                return False
        return True
#_____INIT/GET/RNT_____



#________CONNEXION UDP________
    def initSock(self):
        self.sockBroadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sockBroadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockBroadcast.bind((LOCAL_ADDRESS, self.port))
        self.sockBroadcast.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(LOCAL_ADDRESS))
        self.sockMessage = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sockMessage.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockMessage.bind((LOCAL_ADDRESS, self.port))
        self.sockMessage.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(LOCAL_ADDRESS))
        self.sockMessage.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(GROUP_ADDRESS) + socket.inet_aton(LOCAL_ADDRESS))

    def startConnection(self):
        self.isRunning = True
        self.initSock()
        thread_receive = threading.Thread(target=self.receiveMessage)
        thread_sendRoom = threading.Thread(target=self.sendRoomInfo)
        thread_receive.start()
        thread_sendRoom.start()
        
    def connectNewPort(self, admin, code):
        self.nodeShutDown()
        self.port = code
        c.nbr_lan_player = 0
        self.inRoom = True
        self.admin = admin
        for i in range(len(self.lstRooms)):
            if self.lstRooms[i][0] == code:
                self.roomName = self.lstRooms[i][2]
        self.startConnection()

    def nodeShutDown(self):
        self.isRunning = False
        self.sendMessage("System", f"RemPlayer {self.id}")
        if self.id == 0:
            self.sendMessage("Room", f"DelRoom {self.port}", port=c.init_Port)
        self.inRoom = False
        self.admin = False
        self.id = -1
        self.nbrmessage = 0
        self.port = c.init_Port
#________CONNEXION UDP________



#_________GESTION MESSAGE_________
    def checkNumMsg(self, message):
        if message["port"] != self.port:
            return False
        message["id"] -= 1
        if message["id"] == self.id or self.id < 0 or message["id"] < 0:
            message["id"] += 1
            return True
        idMsg = message["id"]
        if len(self.compteurMsg[message["marque"]]) <= idMsg:
            while len(self.compteurMsg[message["marque"]]) <= idMsg:
                self.compteurMsg[message["marque"]].append(0)
        if message["nbrMessage"] <= self.compteurMsg[message["marque"]][idMsg]:
            return False
        self.compteurMsg[message["marque"]][idMsg] = message["nbrMessage"]
        self.compteurMsg["Time"][idMsg] = int(message["time"])
        message["id"] += 1
        return True

    def sendMessage(self, marque, message, port=None):
        """
        marque: Room/System/Text/InGame
        """
        if self.id >= 0:
            self.compteurMsg[marque][self.id] += 1 
        if port == None:
            port = self.port
        message = f"{port}, {LOCAL_ADDRESS}, {self.id+1}, {self.compteurMsg[marque][self.id]}, {time.time()}, {marque}, {message}"
        self.sockBroadcast.sendto(message.encode("utf8"), (GROUP_ADDRESS, port))

    def readMessage(self, message):
        """
        Renvoie le message sous la forme d'un dico:
        {
            "port": int
            "address": str
            "id": int
            "nbrMessage": int
            "time": float
            "marque": str
            "message": list de str
        }
        """
        if type(message) == bytes:
            message.decode("utf8")
        decode = {}
        message = message.split(", ")
        decode["port"] = int(message[0])
        decode["address"] = message[1]
        decode["id"] = int(message[2])
        decode["nbrMessage"] = int(message[3])
        decode["time"] = float(message[4])
        decode["marque"] = message[5]
        decode["message"] = message[6].split(' ')
        return decode

    def debugPrint(self, entete, message):
        """
        affiche en mettant en forme le message de type dico
        entete: str afficher au tout debut comme un message d'erreur 
        """
        msg = ""
        msg+= "┌┬--------------------------------------------\n"
        msg+=f"|| {entete} :\n"
        msg+= "├┼------------┬------┬------------------------\n"
        for cle in message:
            msg+=f"|| {cle.center(10, ' ')} |{type(message[cle]).__name__.center(6, ' ')}| {message[cle]}\n"
        msg+= "├┼------------┼------┼------------------------\n"
        msg+= "├┼------------┼------┴------------------------\n"
        msg+=f"||     id     | {self.id}\n"
        for cle in self.compteurMsg:
            msg+=f"|| {cle.center(10, ' ')} | {self.compteurMsg[cle]}\n"
        msg+= "└┴------------┴-------------------------------\n"
        print(msg)

    def sendRoomInfo(self):
        while self.isRunning:
            if self.admin:
                self.sendMessage("Room", f"RoomInfo {self.port} {c.nbr_lan_player} {self.roomName}", c.init_Port)
                self.sendMessage("Room", f"ActuConstanteLan {c.nbr_lan_player} {c.max_lape} {c.carte} {''.join(str(int(bo)) for bo in self.lstready)}")
            
                for i in range(len(self.compteurMsg["Time"])):
                    if self.delta < self.compteurMsg["Time"][i]+self.delta < time.time():
                        # potentiellement un probleme ???
                        # si le serveur ne recoit pas son propre msg 
                        self.sendMessage("System", f"RemPlayer {i}")
            else:
                self.sendMessage("Text", "")
                for port in self.lstRooms:
                    if port[3]+self.delta < time.time():
                        self.lanDelRoom(["DelRoom", port[0]])
            time.sleep(1)

    def receiveMessage(self):
        self.sendMessage("System", "AddPlayer")
        while self.isRunning:
            data, _ = self.sockMessage.recvfrom(2048)
            message = self.readMessage(data.decode('utf8'))
            if self.checkNumMsg(message):
                if message["marque"] == "Room":
                    self.commandRoom[message["message"][0]](message["message"])
                elif message["marque"] == "System" and self.inRoom:
                    self.commandSystem[message["message"][0]](message["message"])
                elif message["marque"] == "Text" and self.inRoom:
                    msg = ' '.join(message["message"])
                    if len(msg):
                        self.historique.append((message["id"], msg))
                elif message["marque"] == "InGame":
                    self.commandInGame[message["message"][0]](message["message"])
#_________GESTION MESSAGE_________



#_________System command_________
    def sysMaxLape(self, message):
        """
        message: MaxLape nbr_max_lape"""
        c.max_lape = int(message[1])
        self.historique.append(("0", "MAX LAPE NUMBER HAS CHANGED FOR "+message[1]))
        
    def sysAddPlayer(self, message):
        """
        message: AddPlayer
        """
        self.lstready.append(False)
        c.nbr_lan_player += 1
        self.historique.append(("0", "A PLAYER HAS JOIN THE ROOM"))
        if self.admin:
            self.sendMessage("Room", f"ActuConstanteLan {c.nbr_lan_player} {c.max_lape} {c.carte} {''.join(str(int(bo)) for bo in self.lstready)}")

    def sysRemPlayer(self, message):
        """
        message: RemPlayer Id_client
        """
        self.compteurMsg["Time"][int(message[1])] = 0
        self.lstready.pop(int(message[1]))
        for cle in self.compteurMsg:
            self.compteurMsg[cle][int(message[1])] == 0
        c.nbr_lan_player -= 1
        if int(message[1]) < self.id:
            self.id -= 1
        if self.id == 0:
            self.admin = True
            self.historique.append(("0", "THERE IS A NEW GAME MASTER"))
        self.historique.append(("0", "A PLAYER HAS LEFT THE ROOM"))

    def sysMapChange(self, message):
        """
        message: MapChange nom de la map
        """
        c.carte = ' '.join(message[1:])
        self.historique.append(("0", "THE RACE HAS CHANGED"))
        
    def sysAddReady(self, message):
        """
        message: AddReady Id_client True/False
        """
        self.lstready[int(message[1])] = eval(message[2]) 
#_________System command_________



#___________Room___________
    def lanActuConstanteLan(self, message):
        """
        message: ActuConstanteLan nbr_lan_player max_lape nom de la carte lstReady(ex: 0110)
        """            
        if c.nbr_lan_player > int(message[1]):
            # pas optimal
            for _ in range(5):
                self.historique.append((0, "ERREUR SYNCRONISATION AVEC CLIENT"))
            # self.sendMessage("System", "AddPlayer")
        else:
            c.nbr_lan_player = int(message[1])
            c.max_lape = int(message[2])
            c.carte = ' '.join(message[3:-1])
            self.lstready = [bool(int(bo)) for bo in message[-1]]
            if self.id < 0:
                self.id = c.nbr_lan_player-1

    def lanNameChange(self, message):
        """
        message: NameChange nom de la nouvelle room
        """
        self.roomName = ' '.join(message[1:])
        self.historique.append(("0", "THE ROOM'S NAME HAS CHANGED"))

    def lanRoomInfo(self, message):
        """
        message: RoomInfo port nbrPlayer nom de la room
        """
        port = int(message[1])
        nbrPlayer = int(message[2])
        nom = ' '.join(message[3:])
        ajout = True
        for i in range(len(self.lstRooms)):
            if self.lstRooms[i][0] == port:
                ajout = False
                self.lstRooms[i][1] = nbrPlayer
                self.lstRooms[i][2] = nom
                self.lstRooms[i][3] = int(time.time())
        if ajout:
            self.lstRooms.append([port, nbrPlayer, nom, int(time.time())])

    def lanDelRoom(self, message):
        """
        message: DelRoom port
        """
        i = 0
        while i < len(self.lstRooms):
            if self.lstRooms[i][0] == int(message[1]):
                self.lstRooms.pop(i)
                i = len(self.lstRooms)
            i += 1
#___________Room___________



#__________InGame__________
    def igStartRace(self, message):
        """
        message: StartRace nbr_lan_player nbr_max_lape tempDebut carte
        """
        c.nbr_player = int(message[1])
        c.max_lape = int(message[2])
        self.timeStart = float(message[3])
        c.carte = ' '.join(message[4:])
        self.inGame = True
        self.inWin = False
        self.lstFinish = []
        self.lstready = [False for _ in range(len(self.lstready))]
    
    def igCarMove(self, message):
        """
        message: CarMove id x y degre
        """
        self.CarMovement.append([int(message[1]), float(message[2]), float(message[3]), int(message[4])])

    def igCarFinish(self, message):
        """
        message: CarFinish carId time
        """
        num, t = int(message[1]), float(message[2])
        find = False
        i = 0
        while not(find) and i < len(self.lstFinish):
            find = (self.lstFinish[i][0] == num)
            i += 1
        if not(find):
            self.lstFinish.append((num, t))

    def igSwitchWin(self, message):
        """
        message: SwitchWin
        """
        self.CarMovement = []
        self.inGame = False
        self.inWin = True
#__________InGame__________