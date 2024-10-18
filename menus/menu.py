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

class Menu:
    def __init__(self, nom, actif):
        self.actif = actif
        self.nom = nom

    def get_actif(self):
        return self.actif
    
    def reverse_actif(self):
        self.actif = not(self.actif)

    def set_nom(self, nom):
        self.nom = nom

    def get_nom(self):
        return self.nom
    