"""
Module de jeu en réseaux
"""


import game_client.Web_client as Wb
from game_client.ClientExceptions import * 
from game_client.User import User


#### Exceptions

class GameDontExist(Exception):
    def __init__(self, *args):
        super().__init__(*args)
    
class GameFull(Exception):
    def __init__(self, *args):
        super().__init__(*args)


#### Variables
game_list = {}

game_id = ""

opponent = ""


def get_game_list()->str:
    """Cette fonction permet de retourner un tableau correspondant à une liste de partie, et de lier ces parties à un numéro

    Returns:
        str: La représentation en string du tableau des parties
    """
    #vider l'ancienne liste
    global game_list
    game_list.clear()
    
    #Faire la requête
    req = Wb.web_client.get("https://api.nsi.quark-dev.com/games")
    
    #traiter la requête
    resp : dict = req.json()
    
    game_str=""
    
    i = 1
    for game in resp.keys():
        game_str += f"  {i}- {resp[game]}\n"
        game_list[str(i)] = game
        i += 1
        
    return game_str

def create_game():
    """Cette fonction permet de créer une partie qui peut être rejoin par quelqu'un d'autre
    """
    
    #Faire la requête
    req = Wb.web_client.post("https://api.nsi.quark-dev.com/games")
    
    #Récupérer l'id de la partie
    global game_id
    game_id = req.text
    

def get_status()->dict:
    """Retourne le status général de la partie actuelle
    """
    global game_id
    
    req = Wb.web_client.get(f"https://api.nsi.quark-dev.com/game/{game_id}")
    
    return req.json()
    
def join_game(id):
    """Une fonction qui permet de rejoindre une partie
    """
    
    req = Wb.web_client.get(f"https://api.nsi.quark-dev.com/join/{id}")
    
    #Traiter la réponse
    if req.text == "This game do not exist":
        raise GameDontExist
    
    if req.text == "This game is full":
        raise GameFull
    
    elif req.text == "Successfully joined the game !":
        global game_id
        game_id = id
        

def send_status(user:User):
    """Fonction qui envoie le status de la partie au serveur pour evaluation

    Args:
        user (User): L'utilisateur actuel
    """

    req = Wb.web_client.post("https://api.nsi.quark-dev.com/play/"+game_id, json=user.to_json())
    return req.text
    
def get_infos():
    """Fonction qui demande le status de la partie, ainsi que les données de l’adversaire
    """
    global game_id
    
    req = Wb.web_client.get(f"https://api.nsi.quark-dev.com/infos/{game_id}")
    
    return req.json()
    