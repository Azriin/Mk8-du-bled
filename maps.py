class Course_1:
    def __init__(self):
        self.i = 1
                            #x, y, w, h, num, (point_dist(x, y))
        self.separateur = [(84, 190, 93, 65, 0, (176, 221)),
                           (177, 190, 78, 65, 1, (225, 190)),
                           (103, 128, 152, 62, 2, (142, 128)),
                           (91, 78, 164, 50, 3, (225, 78)),
                           (183, 1, 72, 77, 4, (183, 34)),
                           (134, 1, 49, 58, 5, (134, 34)),
                           (84, 1, 50, 58, 6, (84, 34)),
                           (1, 1, 83, 58, 7, (30, 58)),
                           (1, 59, 83, 19, 8, (32, 77)),
                           (1, 78, 71, 50, 9, (35, 127)),
                           (1, 128, 83, 62, 10, (40, 189)),
                           (1, 190, 83, 65, 11, (83, 221))]
                        #x, y, w, h
        self.bordure = [(0, 0, 1, 256),#mur gauche
                        (1, 0, 255, 1),#toit
                        (255, 0, 1, 256), #mur droit
                        (1, 255, 255, 1), #sol
                        (84, 59, 99, 19),
                        (72, 78, 19, 50),
                        (84, 128, 19, 62),
                        (96, 190, 81, 10)]
    
    def get_indice(self):
        return self.i
    
    def get_separateur(self):
        return self.separateur
    
    def get_bordure(self):
        return self.bordure
    
class Course_2:
    def __init__(self):
        self.i = 2
        self.separateur = [(1, 1, 117, 48, 0, (57, 48)),
                           (1, 49, 104, 26, 1, (74, 74)),
                           (1, 75, 136, 76, 2, (36, 150)),
                           (1, 151, 90, 32, 3, (24, 182)),
                           (1, 183, 74, 72, 4, (74, 224)),
                           (75, 167, 47, 88, 5, (121, 201)),
                           (122, 150, 37, 105, 6, (158, 181)),
                           (159, 150, 96, 105, 7, (221, 150)),
                           (159, 75, 96, 75, 8, (202, 75)),
                           (171, 1, 84, 74, 9, (230, 5)),
                           (118, 1, 53, 48, 10, (118, 24))]

        self.bordure = [(0, 0, 1, 256),#mur gauche
                        (1, 0, 255, 1),#toit
                        (255, 0, 1, 256), #mur droit
                        (1, 255, 255, 1), #sol
                        (6, 45, 16, 16),
                        (30, 79, 16, 16),
                        (54, 98, 16, 16),
                        (59, 183, 16, 16),
                        (75, 167, 16, 16),
                        (141, 210, 16, 16),
                        (180, 149, 16, 16),
                        (227, 92, 16, 16),
                        (91, 151, 31, 16),
                        (122, 135, 37, 16),
                        (105, 49, 66, 26),
                        (137, 75, 22, 60)]
        
    def get_indice(self):
        return self.i

    def get_separateur(self):
        return self.separateur
    
    def get_bordure(self):
        return self.bordure
    
class Course_3:
    def __init__(self):
        self.i = 3
                            #x, y, w, h, num, (point_dist(x, y))
        self.separateur = [(89, 187, 42, 68, 0, (89, 217)),
                           (1, 187, 88, 68, 1, (61, 187)),
                           (1, 148, 88, 39, 2, (45, 148)),
                           (1, 108, 80, 40, 3, (35, 108)),
                           (1, 76, 88, 32, 4, (49, 76)),
                           (1, 52, 120, 24, 5, (72, 52)),
                           (25, 1, 96, 51, 6, (120, 26)),
                           (121, 1, 64, 51, 7, (184, 26)),
                           (185, 1, 70, 51, 8, (229, 51)),
                           (153, 52, 102, 32, 9, (203, 83)),
                           (129, 84, 126, 40, 10, (153, 123)),
                           (129, 124, 64, 64, 11, (192, 162)),
                           (193, 132, 62, 56, 12, (228, 187)),
                           (196, 188, 59, 67, 13, (196, 218)),
                           (145, 196, 51, 59, 14, (145, 217)),
                           (131, 187, 14, 68, 15, (131, 217))]
                        #x, y, w, h
        self.bordure = [(0, 73, 1, 183),#mur gauche
                        (89, 0, 167, 1),#toit
                        (255, 0, 1, 256), #mur droit
                        (1, 255, 255, 1), #sol
                        (0, 65, 9, 8),
                        (9, 57, 8, 8),
                        (17, 49, 8, 8),
                        (25, 41, 16, 8),
                        (41, 33, 8, 8),
                        (49, 25, 8, 8),
                        (57, 17, 16, 8),
                        (73, 9, 8, 8),
                        (81, 0, 8, 9),
                        (193, 124, 62, 8),
                        (144, 188, 51, 8),
                        (97, 188, 32, 8),
                        (89, 148, 8, 40),
                        (129, 180, 16, 8),
                        (129, 164, 8, 16),
                        (81, 140, 8, 8),
                        (73, 132, 8, 8),
                        (65, 108, 8, 24),
                        (73, 92, 8, 16),
                        (129, 92, 8, 16),
                        (121, 108, 8, 56),
                        (81, 84, 8, 8),
                        (137, 84, 8, 8),
                        (89, 76, 8, 8),
                        (145, 76, 8, 8),
                        (97, 68, 8, 8),
                        (153, 68, 8, 8),
                        (105, 60, 16, 8),
                        (161, 60, 8, 8),
                        (121, 52, 64, 8)]
    
    def get_indice(self):
        return self.i
    
    def get_separateur(self):
        return self.separateur
    
    def get_bordure(self):
        return self.bordure