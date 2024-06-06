import pyxel

class Bouton_slide:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = BigTexte(x+16, y+4, text)
        #anim
        self.speed = 5
        self.current_x = x
        self.max_x = x + 25
        
    def draw(self):
        pyxel.blt(self.current_x, self.y, 0, 175, 0, 81, 23, 4)
        self.text.draw()

    def contacte(self):
        return self.x <= pyxel.mouse_x <= 81+ self.max_x and self.y <= pyxel.mouse_y <= self.y + 23

    def animation(self):
        if self.contacte():
            if self.current_x < self.max_x:
                self.current_x += self.speed  
                self.text.setCoo(self.text.getX()+self.speed, self.text.getY())
        else:
            if self.current_x > self.x:
                self.current_x -= self.speed
                self.text.setCoo(self.text.getX()-self.speed, self.text.getY())

    def clic(self):
        return self.contacte() and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)
    
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
            self.couleur = self.col_over
        else : self.couleur = self.col_out

    def clic(self):
        return self.contacte() and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)

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

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 226+15*self.img, 23, 15, 15, 4)

    def clic(self):
        if self.last_clic +self.couldown <= pyxel.frame_count:
            self.last_clic = pyxel.frame_count
            return self.contacte() and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)

    def contacte(self):
        return self.x <= pyxel.mouse_x <= self.x + 15 and self.y <= pyxel.mouse_y <= self.y + 15
    
    def edit_y(self, new_y):
        self.y = new_y

    def animation(self):
        if self.contacte():
            pyxel.circb(self.x+7, self.y+7, 8, self.col_over)

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
        'Z': (206, 241), ':': (216, 241), ' ': (226, 241),
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

    def draw(self):
        pyxel.elli(self.x, self.y, 23, 23, self.couleur)
        pyxel.rect(self.x+9, self.y, self.text.getLen()-2, 23, self.couleur)
        pyxel.elli(self.x+self.text.getLen()-7, self.y, 23, 23, self.couleur)
        self.text.draw()

    def contacte(self):
        return self.x <= pyxel.mouse_x <= self.x+self.text.getLen()+16 and self.y <= pyxel.mouse_y <= self.y + 23
    
    def clic(self):
        return self.contacte() and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)
    
    def animation(self):
        if self.contacte():
            self.couleur = self.col_in
        else : self.couleur = self.col_out