import pyxel

class Bouton_slide:
    def __init__(self, x, y, text, speed=5, max_x=25):
        assert pyxel.sgn(speed) == pyxel.sgn(max_x) and max_x%speed==0, f"{pyxel.sgn(speed) == pyxel.sgn(max_x)}, {max_x//speed==0}"
        self.x = x
        self.y = y
        self.text = BigTexte(x+16, y+4, text)
        #anim
        self.speed = speed
        self.current_x = x
        self.max_x = x + max_x
        #sond
        self.playable = False


    def draw(self):
        pyxel.blt(self.current_x, self.y, 0, 175, 0, pyxel.sgn(self.speed)*81, 23, 4)
        self.text.draw()

    def contacte(self):
        if self.speed >= 0:
            return self.x <= pyxel.mouse_x <= 81+ self.max_x and self.y <= pyxel.mouse_y <= self.y + 23
        else:
            return self.max_x <= pyxel.mouse_x <= 81 + self.x and self.y <= pyxel.mouse_y <= self.y + 23

    def animation(self):
        if self.contacte():
            if self.playable:
                pyxel.play(0, 1)
                self.playable = False
            if self.current_x != self.max_x:
                self.current_x += self.speed  
                self.text.setCoo(self.text.getX()+self.speed, self.text.getY())
        else:
            self.playable = True
            if self.current_x != self.x:
                self.current_x -= self.speed
                self.text.setCoo(self.text.getX()-self.speed, self.text.getY())

    def clic(self):
        isClic = self.contacte() and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
        if isClic:
            pyxel.play(0, 0)
        return isClic
    
class Bouton_radio:
    def __init__(self, x, y, actif, taille, col_over=7, col_out=0, carre=True, cercle=False):
        assert carre != cercle
        #position en haut a gauche
        self.x = x
        self.y = y
        #esthetique
        self.taille = taille
        self.col_over = col_over
        self.col_out = col_out
        self.couleur = self.col_out
        #forme
        self.carre = carre
        self.cercle = cercle

        self.actif = actif
        self.last_clic = 0
        self.wait = 5

        self.playable = True

    def draw(self):
        if self.carre:
            pyxel.rectb(self.x, self.y, self.taille, self.taille, self.couleur)
        if self.cercle:
            pyxel.circb(self.x-self.taille/2, self.y-self.taille/2, self.taille/2, self.couleur)
        if self.actif:
            pyxel.rect(self.x+1, self.y+1, self.taille-2, self.taille-2, self.col_over)

            pyxel.line(self.x+1, self.y+1, self.x + self.taille-2, self.y + self.taille-2, 7)
            pyxel.line(self.x+1, self.y+2, self.x + self.taille-3, self.y + self.taille-2, 0)
            pyxel.line(self.x+2, self.y+1, self.x + self.taille-2, self.y + self.taille-3, 0)
            
            pyxel.line(self.x+1, self.y + self.taille-3, self.x + self.taille-3, self.y+1, 0)
            pyxel.line(self.x+2, self.y + self.taille-2, self.x + self.taille-2, self.y+2, 0)
            pyxel.line(self.x+1, self.y + self.taille-2, self.x + self.taille-2, self.y+1, 7)

            pyxel.pset(self.x+1, self.y+1, 0)
            pyxel.pset(self.x+self.taille-2, self.y+1, 0)
            pyxel.pset(self.x+1, self.y+self.taille-2, 0)
            pyxel.pset(self.x+self.taille-2, self.y+self.taille-2, 0)

    def animation(self):
        if self.contacte():
            if self.playable:
                pyxel.play(0, 1)
                self.playable = False
            self.couleur = self.col_over
        else : 
            self.couleur = self.col_out
            self.playable = True

    def clic(self):
        isClic = self.contacte() and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
        if isClic:
            pyxel.play(0, 0)
        return isClic

    def contacte(self):
        return self.x <= pyxel.mouse_x <= self.x + self.taille and self.y <= pyxel.mouse_y <= self.y + self.taille
    
    def reverse(self):
        if self.last_clic + self.wait <= pyxel.frame_count: 
            self.actif = not(self.actif)
            self.last_clic = pyxel.frame_count

class bouton_poussoir:
    def __init__(self, x, y, img, col_over):
        self.x = x
        self.y = y
        self.last_clic = 0
        self.couldown = 1
        self.img = img
        self.col_over = col_over

        self.playable = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 226+15*self.img, 23, 15, 15, 4)

    def clic(self):
        if self.last_clic +self.couldown <= pyxel.frame_count:
            self.last_clic = pyxel.frame_count
            isClic = self.contacte() and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) 
            if isClic:
                pyxel.play(0, 0)
            return isClic

    def contacte(self):
        return self.x <= pyxel.mouse_x <= self.x + 15 and self.y <= pyxel.mouse_y <= self.y + 15
        
    def edit_y(self, new_y):
        self.y = new_y

    def animation(self):
        if self.contacte():
            if self.playable:
                pyxel.play(0, 1)
                self.playable = False
            pyxel.circb(self.x+7, self.y+7, 8, self.col_over)
        else:
            self.playable = True

class BigTexte:
    def __init__(self, x, y, texte):
        self.x = x
        self.y = y
        self.w = 10
        self.h = 15
        self.dicoLettre = {
        'A': (206, 166), 'B': (216, 166), 'C': (226, 166), 'D': (236, 166), 'E': (246, 166),
        'F': (206, 181), 'G': (216, 181), 'H': (226, 181), 'I': (236, 181), 'J': (246, 181),
        'K': (206, 196), 'L': (216, 196), 'M': (226, 196), 'N': (236, 196), 'O': (246, 196),
        'P': (206, 211), 'Q': (216, 211), 'R': (226, 211), 'S': (236, 211), 'T': (246, 211),
        'U': (206, 226), 'V': (216, 226), 'W': (226, 226), 'X': (236, 226), 'Y': (246, 226),
        'Z': (206, 241), ':': (216, 241), ' ': (226, 241), '|': (236, 241), '-': (246, 241),
        '0': (216, 71), '1': (226, 71), '2': (236, 71), '3': (246, 71),
        '4': (216, 86), '5': (226, 86), '6': (236, 86), '7': (246, 86),
        '8': (216, 101), '9': (226, 101)
        }
        self.text = texte.upper()
        self.verifTxt()

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def getText(self):
        return self.text

    def setCoo(self, x, y):
        self.x = x
        self.y = y

    def setText(self, text):
        self.text = text.upper()

    def verifTxt(self):
        for lettre in self.text:
            assert lettre in self.dicoLettre, "fonction prend uniquement les lettres de A-Z et 0-9 blanc et :"

    def draw(self):
        for i in range(len(self.text)):
            lettre = self.dicoLettre[self.text[i]]
            pyxel.blt(self.x+i*11, self.y, 0, lettre[0], lettre[1], self.w, self.h, 4)

    def getLen(self):
        return 11*len(self.text)-1

class TextButton:
    def __init__(self, x, y, text, col_in, col_out):
        self.x = x
        self.y = y
        self.text = BigTexte(self.x+8, self.y+4, text)
        self.col_in = col_in
        self.col_out = col_out
        self.couleur = self.col_out

        self.playable = True

    def draw(self):
        pyxel.elli(self.x, self.y, 23, 23, self.couleur)
        pyxel.rect(self.x+9, self.y, self.text.getLen()-2, 23, self.couleur)
        pyxel.elli(self.x+self.text.getLen()-7, self.y, 23, 23, self.couleur)
        self.text.draw()

    def contacte(self):
        return self.x <= pyxel.mouse_x <= self.x+self.text.getLen()+16 and self.y <= pyxel.mouse_y <= self.y + 23
    
    def clic(self):
        isClic = self.contacte() and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
        if isClic:
            pyxel.play(0, 0)
        return isClic
    
    def animation(self):
        if self.contacte():
            if self.playable:
                pyxel.play(0, 1)
                self.playable = False
            self.couleur = self.col_in
        else : 
            self.couleur = self.col_out
            self.playable = True

class Entry:
    def __init__(self, x, y, maxVal, text="", selection=False, col=12, frequence=30, littleTxt=False):
        self.x = x
        self.y = y
        self.maxVal = maxVal
        self.w = (self.maxVal*11-3) if not(littleTxt) else (self.maxVal*4+3)
        if not(littleTxt):
            self.textAffich = BigTexte(self.x+8, self.y+4, "")
        self.text = text
        self.selection = selection
        self.col = col
        self.frequence = frequence
        self.littleTxt = littleTxt

    def draw(self):
        if not(self.littleTxt):
            pyxel.elli(self.x, self.y, 23, 23, self.col)
            pyxel.rect(self.x+9, self.y, self.w, 23, self.col)
            pyxel.elli(self.x+self.w-5, self.y, 23, 23, self.col)
            if self.selection and pyxel.frame_count%self.frequence < self.frequence//2:
                self.textAffich.setText(self.text+'|')
            else:self.textAffich.setText(self.text)
            self.textAffich.draw()
        else:
            if self.selection and pyxel.frame_count%self.frequence < self.frequence//2:
                pyxel.text(self.x+2, self.y+3, self.text+'|', 0)
            else:pyxel.text(self.x+2, self.y+3, self.text, 0)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if not(self.littleTxt):
                self.selection = self.x <= pyxel.mouse_x <= self.x+self.w+18 and self.y <= pyxel.mouse_y <= self.y+23
            else: self.selection = self.x-2 <= pyxel.mouse_x <= self.x+self.w+10 and self.y-3 <= pyxel.mouse_y <= self.y+11
        if self.selection:
            if pyxel.btnp(pyxel.KEY_BACKSPACE):
                if pyxel.btn(pyxel.KEY_CTRL):
                    self.text = ""
                else : self.text = self.text[:-1]
            if self.maxVal > len(self.text):
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.text += " "
                for lettre in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                    if pyxel.btnp(eval("pyxel.KEY_"+lettre)):
                        if self.littleTxt and not(pyxel.btn(pyxel.KEY_SHIFT)):
                            self.text += lettre.lower()
                        else: self.text += lettre

    def getText(self):
        return self.text
    
    def setText(self, text):
        self.text = text

class BoutonImage:
    def __init__(self, x, y, matriceOFF, matriceON=None):
        """
        matrice = [u, v, w, h]\n
        u = coo x sur l'image 0\n
        v = coo y sur l'image 0\n
        w = largeur zone \n
        h = hauteur zone\n
        """
        self.x = x
        self.y = y
        self.matriceOFF = matriceOFF
        self.matriceON = matriceON
        self.actif = False

    def centrer(self, m1, m2):
        # d'ou -1//2 == -1 putain
        self.x += int((m1[2] - m2[2])/2)
        self.y += int((m1[3] - m2[3])/2)
            

    def getActif(self):
        return self.actif

    def draw(self):
        if (self.actif and self.matriceON != None):
            pyxel.blt(self.x, self.y, 0, *self.matriceON, 4)
        else :
            pyxel.blt(self.x, self.y, 0, *self.matriceOFF, 4)

    def contacte(self):
        matrice = self.matriceON if (self.actif and self.matriceON != None) else self.matriceOFF
        return self.x <= pyxel.mouse_x <= self.x + matrice[2] and self.y <= pyxel.mouse_y <= self.y + matrice[3]
        
    def clic(self):
        isClic = self.contacte() and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
        if isClic:
            pyxel.play(0, 0)
        return isClic

    def update(self):
        if (self.clic()):
            if (self.actif):
                self.centrer(self.matriceON, self.matriceOFF)
            else:
                self.centrer(self.matriceOFF, self.matriceON)
            self.actif = not(self.actif)
            