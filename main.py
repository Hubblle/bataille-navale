import os

"""
Jeu de Bataille-navale

ALPHA 2

Fonctions:
- Affichage du plateau de jeu avec information de coordination
- Affichage des bateaux sur 4 axes
- Affichage des tirs réussis ou ratés
- Calcul du score
- Définir une victoire à partir d'un score

Fonction de la boucle principale:
- Placement interactif des bateaux
- Tir interactif
- Evaluation du tir

"""

####################
#### Constantes ####
####################

SIGN_DICT={
    "WATER" : '□ ', #Fond du tableau
    "MISSED" : '□ ', # Tir raté
    "TOUCHED" : '⨂ ', # Tir touché
    "SHIP" : '■ ', # Bateau
    "SANK_SHIP" : '▨ '
}


COT = 12 #Taille de coté du tableau



#Dictionnaire utilisé pour tracer les bateaux
#Décris l'operation à appliquer sur les coordonnées de départ selon la direction choisie
DIR = [
    [0, -1], # Nord
    [0,1], # Sud
    [1, 0], # Est
    [-1,0]  # Ouest
]

LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]


#Ici le r evite les cratères échappatoires
logo = r"""
$$$$$$$\             $$\               $$\ $$\ $$\                                                         $$\           
$$  __$$\            $$ |              \__|$$ |$$ |                                                        $$ |          
$$ |  $$ | $$$$$$\ $$$$$$\    $$$$$$\  $$\ $$ |$$ | $$$$$$\         $$$$$$$\   $$$$$$\ $$\    $$\ $$$$$$\  $$ | $$$$$$\  
$$$$$$$\ | \____$$\\_$$  _|   \____$$\ $$ |$$ |$$ |$$  __$$\        $$  __$$\  \____$$\\$$\  $$  |\____$$\ $$ |$$  __$$\ 
$$  __$$\  $$$$$$$ | $$ |     $$$$$$$ |$$ |$$ |$$ |$$$$$$$$ |       $$ |  $$ | $$$$$$$ |\$$\$$  / $$$$$$$ |$$ |$$$$$$$$ |
$$ |  $$ |$$  __$$ | $$ |$$\ $$  __$$ |$$ |$$ |$$ |$$   ____|       $$ |  $$ |$$  __$$ | \$$$  / $$  __$$ |$$ |$$   ____|
$$$$$$$  |\$$$$$$$ | \$$$$  |\$$$$$$$ |$$ |$$ |$$ |\$$$$$$$\        $$ |  $$ |\$$$$$$$ |  \$  /  \$$$$$$$ |$$ |\$$$$$$$\ 
\_______/  \_______|  \____/  \_______|\__|\__|\__| \_______|$$$$$$\\__|  \__| \_______|   \_/    \_______|\__| \_______|
                                                             \______|                                                    
"""




BOATS = {
    "Destroyer" : [5]
    #"Cruiser" : [3,3],
    #"Navette" : [4]
}





##############################
#### Fonctions génériques ####
##############################

def clear_screen()->None:
    """Une fonction qui permet de vider le terminal
    """
    
    #Execute une commande dans un sous-terminal et renvoie la sortie au terminal actuel, ici, la sortie va vider le terminal
    os.system('clear' if os.name == 'posix' else 'cls')
    # Dans le cas ou le nom du module est posix, on execute clear (comme sous les systems Linux par exemple), dans le cas contraire (Windows) la commande est cls




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
    
    letter = [""]
        
    def convert(num):
        if num <= 25:
            letter[0] += LETTERS[num]
            
        else:
            convert(num//26)
            convert(num%26)
        
    
        
    convert(num)
    return letter[0]
    
def letter_to_num(letter:str)->int:
    """Une fonction qui va convertir une lettre du tableau en nombre

    Args:
        letter (str): La lettre à convertir

    Returns:
        int: le numéro corespondant
    """
    
    return LETTERS.index(letter)+1


def replace_at(board:list[list], x:int, y:int, char:str)->list:
    """Fonction qui remplace le symbole aux coordonnées x;y fournie par le char

    Args:
        board (list[list]): Le tableau
        x (int): La coordonnée x
        y (int): La coordonnée y

    Returns:
        list: La liste modifiée
    """
    
    #Ajuste les valeurs pour les utiliser comme index de liste
    x -= 1
    y -= 1
    
    board[y][x]=char
    
    return board



def make_board(ships:list[list], hits:list[list], sank_ships:list = [],SIGNS : dict = SIGN_DICT, ln:int=COT)->str:
    """Fonction permettant d'afficher le tableau du jeu
    
    Args:
        ships (list): la listes des placements de chaques bateaux
        hits (list): la liste des coups tirés
        sank_ships (list, optionel): la liste des bateaux coulés
        SIGNS (dict, optionel): les symboles a utiliser
        ln (int, optionel) : (length) taille de coté du tableau
        
    Returns:
        str: Le tableau formaté sans header ni footer
    
    """
    
    #Définir les symboles
    WATER = SIGNS["WATER"]
    SHIP = SIGNS["SHIP"]
    TOUCHED = SIGNS["TOUCHED"]
    MISSED = SIGNS["MISSED"]
    SANK_SHIP = SIGNS["SANK_SHIP"]
    
    
    
    #Faire une liste qui représente le tableau
    board = [[WATER]*ln for _ in range(ln)]
    
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
        
    #tracer les bateaux coulés si il y en a
    for ship in sank_ships:
        #Récupérer les coordonnées
        x = ship[2]
        y = ship[3]
        replace_at(board, x, y, SHIP)
        
        #Repetition sur toute la longueur du bateau
        for _ in range(ship[0]-1): #On retire 1 car le premier carré est déjà tracé
            #Appliquer la transformation adaptée à la direction choisie
            x += DIR[ship[1]][0]
            y += DIR[ship[1]][1]
            
            replace_at(board, x, y, SANK_SHIP)
    
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
    """Returns si "l'utilisateur a gagné la partie"

    Args:
        opponent_ships (list[list]): La liste des bateaux de l'adversaire
        hits (list[list]): La liste de ses coups tirés

    Returns:
        bool: Si l'utilisateur a gagné la partie
    """
    
    return (sum(ship[0] for ship in opponent_ships)+5*len(opponent_ships) == get_score(opponent_ships, hits))
    
def title(text:str)->str:
    """Une fonction qui permet de générer des titres encadrés

    Args:
        text (str): Le texte à mettre dans l'encadrement

    Returns:
        str: L'encadrement
    """
    
    return "#"*(len(text)+8) + "\n" + f"### {text} ###\n" +"#"*(len(text)+8) + "\n"
    
        


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


##########################
#### Mécanique du jeu ####
##########################

## Variables

users = {
    "user_1":{
        "name":"",
        "ship" : [],
        "hit" : [],
        "sank_ship": [],
        "score" : 0
        
    },
    "user_2":{
        "name":"",
        "ship" : [],
        "hit" : [],
        "sank_ship": [],
        "score" : 0
        
    }
}




def place_ui(name:str, ship_list:list)->None:
    """Fonction qui permet de définir le placement des bateaux d'un joueur

    Args:
        name (str): Le nom du joueur
        boat_list (list): La liste des bateaux du joueur
    """
    
    def header():
        #Fonction qui affiche les headers du menu
        print(title("Les Bateaux"))
        line(2) 
    
    def infos():
        #Affiche des infos quant au placement des bateaux
        print("## Comment placer un bateau ?\n",
                " -> Entrez la coordonnée de début du bateau\n",
                " -> Entrez la direction du bateau\n",
                "   Les directions sont:\n",
                "    -> 0: ↑\n",
                "    -> 1: ↓\n",
                "    -> 2: →\n",
                "    -> 3: ←\n"
                
              )

    print(f"Bienvenue {name}, nous allons procéder au placement de vos batteaux !")
    print(title("Les Bateaux"))
    line(2)        
    
    liste = ""
    for boat in BOATS:
        liste += f" - {boat} -> Longueur {BOATS[boat][0]} (x{len(BOATS[boat])})\n"
    
    print(liste)
    line()
    input("Appuyez sur Entrée pour commencer ↵")

    
    for boat in BOATS:
        
        
        for i in range(len(BOATS[boat])):
            clear_screen()
            header()
            print(f"## Mise en place du {boat} numéro {i+1} ##")
            print(f"-> Longueur = {BOATS[boat][0]}")
            line()
            #affichage du plateau avec les bateaux actuels
            print(make_board(ship_list, []))
            line()
            
            #afficher le tuto
            infos()
            
            #demander le début
            while True:
                cor = input("Entrez les coordonnées du début du bateau (Format: A1) -> ")
                #Traiter l'input
                
                letter = cor[0] #Première lettre
                x = letter_to_num(letter.upper())
                
                y = int(cor[1:])
                
                #Verifier les maximums
                if x > COT:
                    print("Erreur; votre lettre dépasse le maximum !")
                    input("Appuyez sur Entrée pour recommencer ↵")
                
                elif y > COT:
                    print("Erreur votre nombre dépasse le maximum !")
                    input("Appuyez sur Entrée pour recommencer ↵")
                
                elif get_score(ship_list, [[False, x, y]]) != 0:
                    print("Erreur; votre bateau est en collision avec un autre !")
                    input("Appuyez sur Entrée pour recommencer ↵")
                
                else:
                    line()
                    break
                
            #demander la direction
            while True:
                clear_screen()
                header()
                print(f"## Mise en place du {boat} numéro {i+1} ##")
                print(f"-> Longueur = {BOATS[boat][0]}")
                
                line()
                
                print(make_board(ship_list, [[True,x,y]]))
                
                infos()
                
                direc = int(input("Entrez la direction du bateau (0/1/2/3) -> "))
                
                #Verifier que le bateau ne sort pas du plateau
                final_x = x
                final_y = y
                
                colision = False
                for _ in range(BOATS[boat][0]):
                    #Verifier en même temps que le bateau n'en touche pas un autre:
                    if get_score(ship_list, [[True, final_x, final_y]]) != 0: #Le score doit être 0 si le bout du bateau n'en touche pas un autre
                        colision = True
                    
                    #Incrémenter les valeurs
                    final_x += DIR[direc][0]
                    final_y += DIR[direc][1]
                    
                if colision:
                    print("Erreur: Votre bateau touche un autre bateau !")
                    input("Appuyez sur Entrée pour recommencer ↵")
                    continue
                    

                if final_x < 0 or final_x > COT:
                    print("Erreur: Votre bateau sort du plateau !")
                    input("Appuyez sur Entrée pour recommencer ↵")
                    
                elif final_y < 0 or final_y > COT:
                    print("Erreur: Votre bateau sort du plateau !")
                    input("Appuyez sur Entrée pour recommencer ↵")
                    
                
                else:
                    break
            #Ajouter le bateau à la liste:
            ship_list.append([BOATS[boat][0], direc, x, y])
            
    clear_screen()
    header()
    print(f"### {name} Voici le placement de vos bateaux !")
    line()
    print(make_board(ship_list,[]))
    line(2)
    print("Vous pouvez:\n  -> Appuyer sur Entrée pour valider ↵\n  -> Appuyer sur R puis Entrée pour recommencer !")
    entry = input(">>> ")
    
    if entry.capitalize() == "R":
        clear_screen()
        ship_list = [] #vider la liste avant de relancer la fonction
        place_ui(name, ship_list) #Relancer la fonction si le joueur le demande
    
    #Fin de la fonction si l'utilisateur ne souhaite par recommencer
        
def shoot_ui(name:str, ship_list:list, hit:list, opponent_hit:list, sank_ship:list)-> list:
    """Fonction qui permet de tirer un missile

    Args:
        name (str): Le nom de l'utilisateur
        ship_list (list): La liste de ses bateaux
        hit (list): La liste de ses tirs
        opponent_hit (list): La liste des tirs de l'adversaire
        sank_ship: la liste des bateaux coulés
    
    Returns:
        list: Le tir non évalué
    """
    
    def header():
        print(title("Session de tir !"))
        line()
        print(f"{name} c'est à vous de tirer votre missile !")
        
        
    def infos():
        print("## Comment tirer un missile ?")
        print("  1. Entrez les coordonnées de la cible (format A1)")
        print("  2. Confirmez les coordonnées et admirez !")
        
    header()
    line()
    infos()
    
    line()
    
    print("## Vos bateaux:")
    print(make_board(ship_list, opponent_hit))
    
    line(2)
    
    print("## Votre plateau de visée :")
    print(make_board([], hit, sank_ship))
    
    
    line()
    
    while True:
        cor = input("Coordonnées >>> ")
        
        #Traiter l'input
                
        letter = cor[0] #Première lettre
        x = letter_to_num(letter.upper())
        
        y = int(cor[1:])
        
        #Verifier les maximums
        if x > COT:
            print("Erreur; votre lettre dépasse le maximum !")
            input("Appuyez sur Entrée pour recommencer ↵")
        
        elif y > COT:
            print("Erreur votre nombre dépasse le maximum !")
            input("Appuyez sur Entrée pour recommencer ↵")
            
        else:
            break
        
    clear_screen()
    header()
    
    line()
    
    print("## Confirmation de tir /!\\")
    
    #Afficher un résumé du tir
    
    #Faire une copie du dictionaire original
    temp_sign = SIGN_DICT.copy()
    
    temp_sign["SHIP"] = "🎇" #Modifier le symbole du bateau pour l'utiliser en tant que pointeur du tir
    
    temp_ship = [[1, 0, x, y]] # Bateau temporaire pour modéliser le tir
    
    print(make_board(temp_ship, hit, sank_ship, temp_sign))
    
    print("Appuyez sur Entrée pour confirmer le lancement du missile; ou entrez 'R' et appuyez sur Entrée pour replacer votre tir")
    
    user_input  = input(">>> ")
    
    if user_input.capitalize() == "R":
        #Boucler dans la fonction
        
        return shoot_ui(name, ship_list, hit, opponent_hit, sank_ship)
    
    return [None, x, y] #Retourne le tir non évalué 
    
    

    
def eval_shot(opponent_ship:list, user:dict, shot:list) -> bool:
    """Fonction qui évalue un tir, elle met la valeur du tir (True/False) dans sa liste et retourne si le tir a touché un bateau

    Args:
        opponent_ship (list): La listes de bateaux adverses
        user (dict): Le dictionaire de l'utilisateur
        shot(list): Le tir à évaluer 

    Returns:
        bool: Si le tir a touché un bateau
    """
    
    #Regardez si il n'y a pas de collision
    if get_score(opponent_ship, [shot]) == 0:
        
        processed_shot = shot.copy()
        #Signal que le tir n'a pas été réussi
        processed_shot[0] = False
        #Ajoute le tir à la liste
        user["hit"].append(processed_shot)
        
        return False
    
    #Sinon, c'est qu'il y a une collision
    
    processed_shot = shot.copy()
    #Signal que le tir a été réussi
    processed_shot[0] = True
    #Ajoute le tir à la liste
    user["hit"].append(processed_shot)
    
    return True



def eval_sank_ships(opponent_ships:list, user:dict)->bool:
    """Fonction qui évalue si un bateau a été coulé

    Args:
        opponent_ship (list): Les bateaux ennemis
        user (dict): Le dictionaire de l'utilisateur

    Returns:
        bool: Si un nouveau bateau a été coulé
    """
    
    #Etablir la liste de tous les bateaux déjà coulés
    pos_list = []
    for ship in user["sank_ship"]:
        pos_list.append([ship[2],ship[3]])
        
    #Etablir la liste des tirs
    hits_pos = []
    for shot in user["hit"]:
        hits_pos.append([shot[1],shot[2]])
    
    
    #Regarder pour chaques bateaux
    for ship in opponent_ships:
        x = ship[2]
        y = ship[3]
        #Regarder si le bateau n'est pas déjà coulé
        if not [x,y] in pos_list:
            counter = 0
            
            #Parcourir le bateau
            for _ in range(ship[0]):
                if [x,y] in hits_pos:
                    counter += 1
                
                #Parcourir le bateau    
                x += DIR[ship[1]][0]
                y += DIR[ship[1]][1]
                    
            if counter == ship[0]:
                #ajouter le bateau
                user["sank_ship"].append(ship)
                return True
    
    return False

        
        
    
        
    


    



if __name__ == "__main__":
    clear_screen()
    
    print(logo)
    print("""#### Bienvenue dans le jeu de Bataille navale !
Répondez aux question quand vous êtes prêt pour commencer.""")
    line(2)
    
    #Demande le nom des utilisateurs
    for i in range(2):
        if i == 0:
            users["user_1"]["name"] = input("Entrez le nom du joueur 1: ")
            line()
        else:
            users["user_2"]["name"] = input("Entrez le nom du joueur 2: ")
    
    
    #Placer les bateaux
    for user in users:
    
        clear_screen()
        place_ui(users[user]["name"], users[user]["ship"])
        clear_screen()


    
    
    clear_screen()
    print(title("Informations"))
    
    print(">>> Tous les bateaux sont placés !")
    line()
    
    print("Le jeu va donc pouvoir commencer, mais avant, voici les règles: ")
    print("  1. Le jeu se déroule en tours-par-tours, les deux joueurs doivent se passer le clavier à la fin de leur tour, et ne pas regarder l'écran lorsque ce n'est pas leur tour.")
    print("  2. À chaque tour, le joueur va choisir une position ou lancer son missile, si il touche un bateau, il peu alors rejouer.")
    print("  3. Un score est établie au cour de la partie;")
    print("     - Un bateau touché vaut 1 point")
    print("     - Un bateau coulé vaut 5 points")
    print("     -> Le score permet un suivi des performances sur plusieurs parties en les additionnant")
    line()
    print("  4. Le premier joueur qui atteins le maximum de score (tous les bateaux coulés gagne la partie)")
    line()
    print(f">>> Le jeu va commencer par {users['user_1']['name']} !")
    input(f"Appuyez sur Entrée pour commencer ↵")

    
    #Boucle principale
    while True:
        for user in users:
            #Définir les variables
            name = users[user]["name"]
            ship = users[user]["ship"]
            hit = users[user]["hit"]
            sank_ship = users[user]["sank_ship"]
            

            opponent_user = users["user_2"] if user == "user_1" else users["user_1"]
            
            
            
            clear_screen()
            
            def header():
                print(title("Tour de "+name))
                print(f"Informations :\n  > Score: "+users[user]["score"])
               
                
            line(3)
            input(f">>> Appuyez sur Entrée lorsque c'est {name} qui a le clavier !")
            
            # Afficher la session de tir
            clear_screen()
            shot = shoot_ui(name, ship, hit, opponent_user["hit"], sank_ship)
            
            #Regarder si le tir a été réussi
            if eval_shot(opponent_user["ship"], users[user], shot):
               pass
                
            
            
                 
            
            
            
        
        
            
    
        
    
    