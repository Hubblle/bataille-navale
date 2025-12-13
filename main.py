"""
Jeu de Bataille-navale

PRE-ALPHA 2

Fonctions:
- Affichage du plateau de jeu avec information de coordination
- Affichage des bateaux sur 4 axes
- Affichage des tirs réussis ou ratés
- Calcul du score
- Définir une victoire à partir d'un score


"""


#### Constantes
COT = 12 #Taille de coté du tableau
WATER = '□ ' #Fond du tableau
MISSED = '□ '
TOUCHED = '⨂ '
SHIP = '■ '


#Dictionnaire utilisé pour tracer les bateaux
#Décris l'operation à appliquer sur les coordonnées de départ selon la direction choisie
DIR = [
    [0, -1], # Nord
    [0,1], # Sud
    [1, 0], # Est
    [-1,0]  # Ouest
]

LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

###################
#### Fonctions ####
###################

def line(n=1)->None:
    """Fonction qui permet le saut de n lignes
    
    Args:
        n (int): Le nombre de lignes
    """
    for i in range(n):print("")


def num_to_letter(num:int)->str:
    """Une fonction qui va convertir un numéro en lettre utilisable sur le tableau

    Args:
        num (int): Le numéro à convertir

    Returns:
        str: La (ou les) lettre(s) correspondant(ent)
    """
    if num <= 26:
        return LETTERS[num]
    
    #TODO: Le faire marcher pour n'importe quel nombre


def replace_at(board:list[list], x:int, y:int, char:str)->list:
    """Fonction qui remplace le symbole aux coordonnées x;y fournie par le char

    Args:
        board (list[list]): Le tableau
        x (int): La coordonnée x
        y (int): La coordonnée y

    Retourne:
        list: La liste modifiée
    """
    
    #Ajuste les valeurs pour les utiliser comme index de liste
    x -= 1
    y -= 1
    
    board[y][x]=char
    
    return board


# draw_board(ln:int=COT)
#                    ^ on définie la valeur sur la constante locale par défaut
def make_board(ships:list[list], hits:list[list], ln:int=COT)->str:
    """Fonction permettant d'afficher le tableau du jeu
    
    Args:
        ln (int, optionel) : (length) taille de coté du tableau
        ships (list): la listes des placements de chaques bateaux
        hits (list): la liste des coups tirés
        
    Retourne:
        str: Le tableau formaté sans header ni footer
    
    """
    #Faire une liste qui représente le tableau
    board = list([WATER]*ln for _ in range(ln))
    
    #tracer chaque bateau
    for ship in ships:
        #Récupérer les coordonnées
        x = ship[2]
        y = ship[3]
        replace_at(board, x, y, SHIP)
        
        #Repetition sur toute la longueur du bateau
        for _ in range(ship[0]-1): #On retire 1 car le premier carré est déjà tracé
            #Appliquer la transformation adaptée à la direction choisie
            x += DIR[ship[1]][0]
            y += DIR[ship[1]][1]
            
            replace_at(board, x, y, SHIP)
            
    #tracer chaque tir
    for hit in hits:
        replace_at(board, hit[1], hit[2], TOUCHED if hit[0] else MISSED)
    
    #Convertir en string
    #Générer la partie haute
    board_string= "    " #Ajuster pour que ce soit aligné avec le tableau
    for num in range(len(board)):
        #Ajout d'une lettre représentative d'un nombre
        board_string += num_to_letter(num)+"|"
        
    board_string+="\n"
        
    
    
    for i in range(len(board)):
        board_string+=f"{i+1:<2}| " # ":<2" On aligne à droite sur deux caractères
        for char in board[i]:
            board_string += char
        board_string += "\n"
     
    return board_string

def get_score(opponent_ships:list[list], hits:list[list])->int:
    """Une fonction qui calcule le score d'un joueur basé sur la position de ses coups tirés et des bateaux de l’adversaire
    Si le score est égal à:
        sum(la longueur de chaques bateaux adverse) + (nombres de bateaux * 5)
    alors l'utilisateur à gagné la partie

    Args:
        opponent_ships (list[list]): La liste des bateaux de l'adversaire
        hits (list[list]): La liste de ses coups tirés

    Returns:
        int: Le score
    """
    score = 0
    
        
    #Etablir la liste des postions de chaques coups tirés
    hits_pos = [[hit[1],hit[2]] for hit in hits]
    
    #Regarder pour chaques bateaux
    for ship in opponent_ships:
        counter = 0
        #Parcourir le bateau
        x = ship[2]
        y = ship[3]
        for _ in range(ship[0]):
            if [x,y] in hits_pos:
                score += 1
                counter += 1
            
            #Parcourir le bateau    
            x += DIR[ship[1]][0]
            y += DIR[ship[1]][1]
                
        if counter == ship[0]:
            #Ajout d'un bonus si tout un bateau est touché
            score += 5
            
    return score

def has_win(opponent_ships:list[list], hits:list[list])->bool:
    """Retourne si l'utilisateur a gagné la partie

    Args:
        opponent_ships (list[list]): La liste des bateaux de l'adversaire
        hits (list[list]): La liste de ses coups tirés

    Returns:
        bool: Si l'utilisateur a gagné la partie
    """
    
    return (sum(ship[0] for ship in opponent_ships)+5*len(opponent_ships) == get_score(opponent_ships, hits))
    


    


######################
#### Informations ####
######################

"""
Format attendu pour la liste des bateaux
[
    #une liste par bateau
    [
        5, #Longueur du bateau
        0/1/2/3, direction du bateau ( 0-N / 1-S / 2-E / 3-W )
        00, coordonnée x de début du bateau
        00, coordonnée y de début du bateau
]


Format attendu pour la liste des tirs
[   
    #une liste par tir
    [
        True/False, #Si le tir a touché un bateau
        00, # coordonnée x
        00, # coordonnée y
    ]
    ]
]

"""

ships=[[5,1,2,1]]

hits = [[True, 2,2],[False, 6, 3], [True, 8, 4],[True,2,1],[True,2,3],[True,2,4],[True,2,5]]

print(make_board(ships,hits))
print("Score: "+str(get_score(ships,hits)))
print("A gagné: ", has_win(ships,hits))