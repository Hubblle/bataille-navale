"""
Module utilisé pour les parties en multi-joueurs réseaux du jeu
"""

from time import sleep
from main import *
import game_client.User as usr
from game_client.ClientExceptions import *
import game_client.game as game
import getpass

lose=r"""
 /$$$$$$$             /$$$$$$          /$$   /$$                          
| $$__  $$           /$$__  $$        |__/  | $$                          
| $$  \ $$  /$$$$$$ | $$  \__//$$$$$$  /$$ /$$$$$$    /$$$$$$             
| $$  | $$ /$$__  $$| $$$$   |____  $$| $$|_  $$_/   /$$__  $$            
| $$  | $$| $$$$$$$$| $$_/    /$$$$$$$| $$  | $$    | $$$$$$$$            
| $$  | $$| $$_____/| $$     /$$__  $$| $$  | $$ /$$| $$_____/            
| $$$$$$$/|  $$$$$$$| $$    |  $$$$$$$| $$  |  $$$$/|  $$$$$$$ /$$ /$$ /$$
|_______/  \_______/|__/     \_______/|__/   \___/   \_______/|__/|__/|__/
                                                                          
"""



user = None

def main_online():
    global user
    
    
    clear_screen()
    print(title("Gestion des comptes"))
    
    #Construire un utilisateur
    user=usr.construct()

    if type(user) == usr.User:
        if not user.get_login():

            line(2)
            print(f"Vous êtes enregistré comme {user.get_login}, mais vous êtes déconnecté !")
            while True:
                mdp = input("Entrez le mot-de-passe de "+user.username+" >>> ")
                
                try:
                    user.login(mdp)
                    
                except WrongCredentials:
                    print("Le mot de passe n'est pas correct /!\\")
                    line(2)
                    continue
                
                break
            
    else:
        print("Avez vous déjà un compte ?")
        
        resp = ""
        while resp not in ["O","N"]:
            resp = input("(O/N) >>> ").capitalize()
        
        if resp == "N":
            while True:
                clear_screen()
                print(title("Inscription"))
                
                line(2)
                print("Entrez le nom d'utilisateur")
                username = input(">>> ")
                
                while True:
                    line()
                    print("Entrez le mot de passe (rien n'est affiché durant la saisie)")
                    mdp = getpass.getpass(">>> ")
                    line()
                    print("Confirmez le mot de passe ")
                    mdp_conf = getpass.getpass(">>> ")
                    
                    if mdp_conf != mdp:
                        print("/!\\ Les deux mots de passes ne corespondent pas ")
                        line()
                        continue
                    
                    break
                
                try:
                    user = usr.register(username, mdp)
                    user.login(mdp)
                except WrongFormat:
                    print("Le format est incorrect (mot de passe ou nom d'utilisateur vide)")
                    input("Appuyez sur entrée pour continuer >> ")
                    continue
                    
                    
                except UserAlreadyExist:
                    print("Ce nom d'utilisateur est déjà pris !")
                    input("Appuyez sur entrée pour continuer >> ")
                    continue
                
                else:
                    break
                
        if resp == "O":
            while True:
                clear_screen()
                print(title("Connexion"))
                
                line(2)
                print("Entrez le nom d'utilisateur")
                username = input(">>> ")
                print("")
                print("Entrez le mot-de-passe (rien n'est affiché durant la saisie)")
                mdp = getpass.getpass(">>> ")

                try:
                    user = usr.User(username)
                    user.login(mdp)
                except WrongCredentials:
                    print("Le mot de passe ou le non d'utilisateur est incorrect !")
                
                else:
                    break
                

    clear_screen()
    print(title("Multijoueur"))
    line()
    print("Vous êtes connecté en tant que "+user.username)
    line(3)
    
    print("#### Menu")
    print("  1- Rejoindre une partie")
    print("  2- Se déconnecter")
    print("  3- Revenir au menu principal")
    print("  4- Créer une partie")
    print("####")
    
    while True:
        line()
        print("Merci de choisir une option [1-4]")
        option = input(">>> ")
        
        if option == "2":
            user.sign_out()
            return main_online()

        if option == "3":
            return main_menu()
        
        
        if not option in ["1", "4"]:
            continue
        break
    
    
    if option == "4":
        create_game()
    
    if option == "1":
        while True:
            clear_screen()
            print(title("Rejoindre une partie"))
            line(2)
            
            print("### Liste des parties;")
            print(game.get_game_list())
            
            line()
            while True:
                print("Merci d'entrer le numéro de la partie que vous voulez rejoindre")
                num = input(">>> ")
                
                #Regarder si le numéro est valide
                game_id = game.game_list.get(num, False)
                if not game_id:
                    continue
                break
            
            try:
                game.join_game(game_id)
            except game.GameDontExist:
                print("Une erreur s'est produite durant la connexion à cette partie ! (GameDontExist error)")
                input("Appuyez sur Entrée pour recommencer ")
                continue
            except game.GameFull:
                print("Une erreur s'est produite durant la connexion à cette partie ! (GameFull error)")
                input("Appuyez sur Entrée pour recommencer ")
                continue
            
            game.opponent = game.get_status().get("creator")
            break
        
    play_game()
                


def create_game():
    """Fonction qui permet de créer une partie et d'attendre pour des joueurs
    """
    clear_screen()
    print(title("En attente de joueur"))

    game.create_game()
    while True:
        sleep(0.5)
        #Si la partie est pleine on affiche le joueur qui a rejoin
        infos = game.get_status()
        if infos.get("full"):
            print(f"-> {infos.get('opponent')} a rejoin !")
            input("Appuyez sur entrée pour commencer à jouer; ")
            break
    game.opponent = infos.get("opponent")
    return play_game()
            
        
def play_game():
    """Fonction principale qui permet de traiter une partie en multijoueur rejoin à partir des fonctions du module 
    """
    global user
    
    clear_screen()
    place_ui(user.username, user.ship)
    game.send_status(user)

    line()
    clear_screen()
    #Afficher les règles
    print("Le jeu va donc pouvoir commencer, mais avant, voici les règles: ")
    print("  1. Le jeu se déroule en tours-par-tours, les deux joueurs doivent se passer le clavier à la fin de leur tour, et ne pas regarder l'écran lorsque ce n'est pas leur tour.")
    print("  2. À chaque tour, le joueur va choisir une position ou lancer son missile, si il touche un bateau, il peu alors rejouer.")
    print("  3. Un score est établi au cour de la partie;")
    print("     - Un bateau touché vaut 1 point")
    print("     - Un bateau coulé vaut 5 points")
    print("     -> Le score permet un suivi des performances sur plusieurs parties en les additionnant")
    line()
    print("  4. Le premier joueur qui atteins le maximum de score (tous les bateaux coulés) gagne la partie")
    line()
    print(f">>> En attente que {game.opponent} place ses bateaux !")

    
    while True:
        sleep(0.5)
        stats = game.get_infos()
        
        #Si l'utilisateur a définie ses bateau la liste n'est plus vide
        if len(stats[game.opponent]["ship"]) != 0:
            break
        
    input("Tous les bateaux on été placés ! Appuyez sur Entrée pour continuer >>> ")
    
    #Boucle principale du jeu
    while True:
        # Récupérer les dernières infos de la partie
        stats = game.get_infos()

        opp_stats = stats.get(game.opponent, {"ship": [], "hit": [], "sank_ship": [], "score": 0})

        #à qui est le tour
        next_turn = stats.get("next_turn")

        # Tour du joueur
        if next_turn == user.username:


            while True:
                # Afficher la session de tir
                user.shot = shoot_ui(user.username, user.ship, user.hit, opp_stats.get("hit", []), game.opponent, len(opp_stats.get("sank_ship", [])), user.sank_ship, stats.get("turn"))


                # Envoyer le nouveau status au serveur
                while True:
                    try:
                        req = game.send_status(user)
                    except Exception:
                        # Refaire
                        continue
                    break
                
                #Traiter la réponse:
                touched = False
                sank = False
                if req == "touched": touched = True
                
                elif req == "sank": sank = True
                
                elif req == "win":
                    clear_screen()
                    line(5)
                    print(victory)
                    line(2)
                    print(f"##### Vous avez gagné ! ####")
                    line()
                    print("-> Bilan de la partie")
                    print("  # Vous")
                    print("    -> Score: "+str(user.score))
                    
                    print("  # "+game.opponent)
                    print("    -> Score: "+str(opp_stats["score"]))
                        
                    line()
                    user_in = input("C'est la fin du jeu, appuyez sur Entrée pour quitter, ou entrez 'R' puis Entrée pour rejouer >>> ")
                    if user_in.capitalize() == 'R':
                        del user
                        return main_online()
                    
                    else:
                        exit()
                                
                else:
                    clear_screen()
                    line(5)
                    print(title("Loupé !"))
                    line()
                    input("Appuyez sur Entrée pour continuer !")
                    # Fin du tour
                    break
                
                
                #Actualiser les données
                if touched or sank:
                    stats=game.get_infos()
                    
                    user.hit = stats[user.username].get("hit")
                    user.sank_ship = stats[user.username].get("sank_ship")
                    user.score = stats[user.username].get("score")
                    
                if touched:
                    clear_screen()
                    line(5)
                    print(title(" Touché !"))
                    print("+1 point")
                    print(f"Votre score: {user.score}")
                    line()
                    input("Vous pouvez rejouer, appuyez sur Entrée pour continuer >>>")
                    continue
                
                elif sank:
                    clear_screen()
                    line(5)
                    print(title(" Coulé !"))
                    print("+6 points")
                    print(f"Votre score: {user.score}")
                    line()
                    input("Vous pouvez rejouer, appuyez sur Entrée pour continuer >>>")
                    continue
                
               

        # Tour de l'adversaire : attendre que le serveur indique le retour du tour
        else:
            clear_screen()
            print(title("En attente"))
            stats = game.get_infos()
            next_turn = stats.get("next_turn")
            

            print(f">>> C'est au tour de {next_turn}. En attente de la fin du tour...")
            # Boucler sur la récupération des infos tant que ce n'est pas notre tour
            while True:
                sleep(0.8)
                stats = game.get_infos()
                
                #Verifier la défaite
                if stats.get("win")[0] == True:
                    clear_screen()
                    line(5)
                    print(lose)
                    line(2)
                    print(f"##### Vous avez perdu.. ####")
                    line()
                    print("-> Bilan de la partie")
                    print("  # Vous")
                    print("    -> Score: "+str(user.score))
                    
                    print("  # "+game.opponent)
                    print("    -> Score: "+str(stats[game.opponent]["score"]))
                        
                    line()
                    user_in = input("C'est la fin du jeu, appuyez sur Entrée pour quitter, ou entrez 'R' puis Entrée pour rejouer >>> ")
                    
                    if user_in.capitalize() == 'R':
                        del user
                        return main_online()
                    
                    else:
                        exit()
                
                next_turn = stats.get("next_turn")

                if next_turn == user.username:
                    break


if __name__ == "__main__":
    main_online()