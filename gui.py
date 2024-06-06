import pyxel
import addon_pyxel
import constante

def tri_insertion(tri_tab):
        for i in range(1, len(tri_tab)):
            v = tri_tab[i]
            j = i
            while (tri_tab[j-1].get_lape() < v.get_lape() if tri_tab[j-1].get_lape() !=v.get_lape()\
                   else tri_tab[j-1].get_part() < v.get_part() if tri_tab[j-1].get_part() != v.get_part()\
                    else tri_tab[j-1].get_dist() > v.get_dist()) and j > 0:
                tri_tab[j] = tri_tab[j-1]
                j -= 1
            tri_tab[j] = v
        return tri_tab

class In_game:
    def __init__(self, players):
        self.players = players
        self.timer = pyxel.frame_count
        self.arret = 1
        self.textTimer = addon_pyxel.BigTexte(123, 118, str(self.arret))
        
    def restart(self, new_players):
        self.players = new_players
        self.timer = pyxel.frame_count

    def draw(self):
        if self.timer + self.arret*30 > pyxel.frame_count:
            self.textTimer.draw()
            if pyxel.frame_count%30 == 0:
                self.textTimer.setText(str(int(self.textTimer.getText())-1))
        else:
            for i in range(len(self.players)):
                pyxel.blt(11 + 61*i, 239, 0, 216+10*i, 56, 10, 15, 4)#position
                pyxel.blt(23 + 61*i, 240, 0, 219, 243, 4, 12, 4)#:
                self.players[i].draw_win(29+61*i, 240)#voiture
                pyxel.blt(47 + 61*i, 240, 0, 219, 243, 4, 12, 4)#:
                addon_pyxel.BigTexte(53 + 61 * i, 239, str(self.players[i].get_lape())).draw()
                if len(self.players) - 1 != i:
                    pyxel.blt(66 + 61*i, 238, 0, 253, 38, 3, 17, 4)#separateur

    def update(self):
        self.players = tri_insertion(self.players)
        if self.timer + self.arret*30 < pyxel.frame_count:
            for car in self.players:
                car.reverse_brake(False)
        else:
            for car in self.players:
                car.reverse_brake(True)
            

class Menu:
    def __init__(self, affiche:bool):
        self.affiche = affiche
        self.titre = (0, 90, 128, 38)
        self.bouton_local = addon_pyxel.Bouton_slide(53, 86, "local")
        self.bouton_quitter = addon_pyxel.Bouton_slide(131, 221, "quit")
        # self.bouton_lan = addon_pyxel.Bouton_slide(75, 124, 2)

    def get_affiche(self):
        return self.affiche
    
    def reverse(self):
        self.affiche = not(self.affiche)

    def draw(self):
        #bg
        pyxel.tri(77, 0, 77, 255, 224, 255, 6)
        pyxel.rect(0, 0, 77, 256, 6)
        #objet
        pyxel.blt(125, 17, 0, *self.titre, 13)
        self.bouton_local.draw()
        self.bouton_quitter.draw()
        # self.bouton_lan.draw()

    def update(self):
        self.bouton_local.animation()
        if self.bouton_local.clic():
            self.reverse()
        self.bouton_quitter.animation()
        if self.bouton_quitter.clic():
            pyxel.quit()
        # self.bouton_lan.animation()
        # if self.bouton_lan.clic():
        #     print("pas encore code")

class Victoire:
    def __init__(self, players, affiche):
        self.players = players
        self.affiche = affiche
        self.titre = addon_pyxel.BigTexte(114, 20, "classement:")
        self.back = addon_pyxel.Bouton_slide(115, 193, "menu")

    def get_affiche(self):
        return self.affiche
    
    def reverse(self):
        self.affiche = not(self.affiche)

    def actu_players(self, new_players):
        self.players = new_players

    def classement(self):
        self.players = tri_insertion(self.players)
        for i in range(len(self.players)):
            pyxel.blt(51, 85 + 24*i, 0, 216+10*i, 56, 10, 15, 4)#num
            pyxel.blt(70, 87 + 24*i, 0, 219, 243, 4, 12, 4)#:
            pyxel.blt(50, 103 + 24*i, 0, 0, 84, 50, 3, 4)#barre
            self.players[i].draw_win(83, 87+24*i)#tuture
        
    def draw(self):
        #bg
        pyxel.tri(77, 0, 77, 255, 224, 255, 6)
        pyxel.rect(0, 0, 77, 255, 6)
        #objet
        self.titre.draw()
        pyxel.blt(138, 41, 0, 10, 113, 69, 9, 13)
        pyxel.blt(114, 37, 0, 0, 87, 112, 3, 4)
        self.back.draw()
        #classement
        self.classement()
        
    def update(self, menu):
        self.back.animation()
        if self.back.clic():
            menu.reverse()
            self.reverse()

class GameMode:
    def __init__(self):
        self.nbr_joueur = 3
        self.tour = 3
        self.mode_facile = False
        self.affiche = True
        self.map = 1
        self.jouer = addon_pyxel.Bouton_slide(130, 219, "jouer")
        self.menu = addon_pyxel.Bouton_slide(145, 4, "menu")
        self.rad_conduite = addon_pyxel.Bouton_radio(9, 230, False, 16, col_over=6)
        self.radtour = {1 : addon_pyxel.Bouton_radio(196, 71, False, 16),
                        3 : addon_pyxel.Bouton_radio(196, 94, True, 16),
                        5 : addon_pyxel.Bouton_radio(196, 117, False, 16)}
        self.add_player = addon_pyxel.bouton_poussoir(13, 27, 0, 11)
        self.rem_player = addon_pyxel.bouton_poussoir(86, 27, 1, 8)
        # textes
        self.texts = {
            "conduite": addon_pyxel.BigTexte(7, 211, "conduite"),
            "facile": addon_pyxel.BigTexte(29, 231, "facile"),
            "joueur:": addon_pyxel.BigTexte(3, 1, "joueur:"),
            "tour:": addon_pyxel.BigTexte(192, 50, "tour:"),
            ":1": addon_pyxel.BigTexte(218, 72, ":1"),
            ":3": addon_pyxel.BigTexte(218, 95, ":3"),
            ":5": addon_pyxel.BigTexte(218, 118, ":5"),
            "carte": addon_pyxel.BigTexte(192, 194, "carte")
        }

    def reverse(self):
        self.affiche = not(self.affiche)

    def get_affiche(self):
        return self.affiche
    
    def get_tour(self):
        return self.tour
    
    def get_nbr_joueur(self):
        return self.nbr_joueur
    
    def draw(self):
        #fond
        pyxel.tri(78, 0, 225, 255, 225, 0, 6)
        pyxel.rect(226, 0, 30, 256, 6)
        #bouttons
        self.jouer.draw()
        self.menu.draw()
        #mode de conduite
        self.texts["conduite"].draw()
        self.texts["facile"].draw()
        self.rad_conduite.draw()#rad conduite
        #joueur
        self.texts["joueur:"].draw()
        pyxel.blt(1, 18, 0, 0, 87, 112, 3, 4)#barre joueur
        if self.nbr_joueur != constante.max_player:
            self.add_player.draw()
        if self.nbr_joueur != constante.min_player:
            self.rem_player.draw()
        for i in range(self.nbr_joueur):
            pyxel.blt(9, 35+i*45, 0, 216+10*i, 56, 10, 15, 4) #numéro
            pyxel.blt(27, 36+45*i, 0, 219, 243, 4, 12, 4)#: entre num et tuture
            pyxel.blt(63, 36+45*i, 0, 219, 243, 4, 12, 4)#: entre tuture et controle
            pyxel.blt(39, 36+45*i, 0, 16*i, 41, 16, 12, 4)#voiture
            pyxel.blt(76, 26+45*i, 0, 32*i, 128, 32, 32, 4)#controle
            pyxel.blt(1, 63+45*i, 0, 0, 87, 112, 3, 4)#barre
        #tour
        self.texts["tour:"].draw()
        self.texts[":1"].draw()
        self.texts[":3"].draw()
        self.texts[":5"].draw()
        for key in self.radtour:
            self.radtour[key].draw()
        #map
        self.texts["carte"].draw()
        pyxel.rectb(195, 144, 48, 48, 13)#cadre
        pyxel.blt(196, 145, 0, 46*self.map, 210, 46, 46)#visualisation

    def update(self, menu, chosemaps, new_map):
        #jouer
        self.jouer.animation()
        if self.jouer.clic():
            self.reverse()
        #back menu
        self.menu.animation()
        if self.menu.clic():
            menu.reverse()
        #mode de conduite
        self.rad_conduite.animation()
        if self.rad_conduite.clic():
            self.rad_conduite.reverse()
            self.mode_facile = self.rad_conduite.actif
        #tour
        for key in self.radtour:
            self.radtour[key].actif = self.tour == key
            self.radtour[key].animation()
            if self.radtour[key].clic():
                self.tour = key
        #joueur
        if self.nbr_joueur != constante.max_player:
            self.add_player.animation()
            self.add_player.edit_y(27 + self.nbr_joueur*45)
            if self.add_player.clic():
                self.nbr_joueur += 1 if self.nbr_joueur < constante.max_player else 0
        if self.nbr_joueur != constante.min_player:
            self.rem_player.animation()
            self.rem_player.edit_y(27 + self.nbr_joueur*45)
            if self.rem_player.clic():
                self.nbr_joueur -= 1 if self.nbr_joueur > constante.min_player else 0
        #map
        self.map = new_map
        if 195 <= pyxel.mouse_x <= 243 and 144 <= pyxel.mouse_y <= 192:
            pyxel.rectb(195, 144, 48, 48, 10)
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                chosemaps.reverse()
                self.reverse()



    def rtn_info(self):
        return [self.nbr_joueur, self.mode_facile, self.tour]
    
class ChoseMaps:
    def __init__(self):
        self.affiche = False
        self.selection = 1
        self.back = addon_pyxel.Bouton_slide(115, 193, "menu")
                            #x menu, y menu, x image, y image, indice
        self.display_maps = [(25, 33, 46, 210, 1),#carte 1
                             (105, 33, 92, 210, 2),#carte 2
                             (185, 33, 0, 210, 0), #rng
                             (25, 113, 138, 210, 3)]# carte 3

    def get_display_maps(self):
        return len(self.display_maps)

    def get_selection(self):
        return self.selection
    
    def get_affiche(self):
        return self.affiche

    def reverse(self):
        self.affiche = not(self.affiche)

    def update(self, menu):
        self.back.animation()
        if self.back.clic():
            menu.reverse()
            self.reverse()
        
        for carte in self.display_maps:
            if carte[0] <= pyxel.mouse_x <= carte[0] + 46 and carte[1] <= pyxel.mouse_y <= carte[1] + 46 and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                self.selection = carte[4]

    def draw(self):
        pyxel.tri(77, 0, 77, 255, 224, 255, 6)
        pyxel.rect(0, 0, 77, 255, 6)
        self.back.draw()
        for carte in self.display_maps:
            #images cartes
            pyxel.blt(carte[0], carte[1], 0, carte[2], carte[3], 46, 46)
            #selecteurs
            col = 13
            if carte[4] == self.selection:
                pyxel.rectb(carte[0]-2, carte[1]-2, 50, 50, 10)
                col = 10
            elif carte[0] <= pyxel.mouse_x <= carte[0] + 46 and carte[1] <= pyxel.mouse_y <= carte[1] + 46:
                col = 8
            pyxel.rectb(carte[0]-1, carte[1]-1, 48, 48, col)