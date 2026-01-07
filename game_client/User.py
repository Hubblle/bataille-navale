"""
Le module utilisateur
C'est la classe principale de ce wrapper de l'api game manager

"""


#imports
import game_client.Web_client as Wb
from game_client.ClientExceptions import * 
from requests import Response


class User():
    def __init__(self, username:str):
        # Initialiser l'utilisateur avec les valeurs données:
        self.username = username
        self.ship = []
        self.hit = []
        self.sank_ship=[]
        self.score=0
        self.shot = None
        
    def to_json(self)->dict:
        """Retourne les données de l'utilisateur sous un format json valide
        """
        return {
            "name":self.username,
            "ship": self.ship,
            "hit": self.hit,
            "sank_ship": self.sank_ship,
            "score": self.score,
            "shot": self.shot
        }
        
        
    def __eq__(self, value):
        # Regarder si deux utilisateurs sont égaux:
        return self.username == value.username
    
    #### Méthodes de l'API
    
    def login(self, password:str):
        """Cette fonction authentifie l'utilisateur donné

        Args:
            password (str): Le mot de passe non hashé

        Raises:
            WrongCredentials: Si le mot de passe ou le nom d'utilisateur n'a pas été accepté
            UnknownResponse: Si la réponse du serveur est inconnue
            
        Returns:
            User: L'objet user correspondant si l'utilisateur est bien authentifié
        """
        #Faire la requête
        req = Wb.web_client.post("https://api.nsi.quark-dev.com/login", {"username":self.username, "password":password})
        
        #Regarder la réponse
        response = req.text
        
        #Regarder si l'utilisateur a été authentifié
        if response == "User logged in !":
            return self
        
        #Sinon quelque chose n'allait pas
        if response == "This user do not exist !" or response == "Wrong login credentials !":
            raise WrongCredentials
        
    
        else:
            #Si la réponse est inconnue
            raise UnknownResponse
        
        

        
    def get_login(self) -> bool:
        """Retourne le status de l'utilisateur

        Raises:
            UnknownResponse: Si la réponse du serveur est invalide

        Returns:
            bool: Le status d'authentification de l'utilisateur
        """
        #Faire la requête
        req = Wb.web_client.get("https://api.nsi.quark-dev.com/login")
        
        
        
        if req.text == "True":
            return True
        elif req.text == "False":
            return False
        
        else:
            raise UnknownResponse



    
    
    def get_username(self)->str|None:
        """Une fonction permettant d'obtenir le nom d'utilisateur de l'utilisateur connecté, s'il y en a un.
        Utilisée pour revenir à l'état de connexion précédent sans avoir à redemander le nom d'utilisateur et le mot de passe après la fermeture de l'application, et sans nécessiter de stockage local.

        Raises:
            UnknownResponse: Si la réponse est inconnue

        Returns:
            str: Le nom d'utilisateur
            None: Ne retourne rien si le nom d'utilisateur est vide
        """
        
        req = Wb.web_client.get("https://api.nsi.quark-dev.com/users")
        
        #traiter la réponse
        return req.text if req.text != "" else None
    
    def sign_out(self):
        """Une fonction qui permet de dé-authentifier l'utilisateur, et de vider les cookies au passage
        """
        Wb.web_client.session.cookies.clear()
        Wb.web_client.save_current_cookies()
        
            
    
    

def construct()->User|None:
    """Fonction qui essaye de reconstruire l'utilisateur tel qui était avant la fermeture du programme

    Returns:
        User|None: Retourne l'utilisateur si il a été construit, sinon None
    """
    
    temp_user = User(None)
    
    username= temp_user.get_username()
    
    if username != None:
        temp_user.username = username
        return temp_user
    
    else:
        return None
    
    


def register(username:str,password:str)->User:
    """Fonction pour enregistrer un nouveau utilisateur
    
    Args:
        username (str): Le nom d'utilisateur
        password (str): Le mot de passe

    Raises:
        WrongFormat: Si le format est mauvais (mot de passe ou nom d'utilisateur invalide)
        UserAlreadyExist: Si le nom d'utilisateur existe déjà
        UnknownResponse: Si la réponse du serveur est inconnue

    Returns:
        User: L'utilisateur si l'enregistrement s'est fait sans erreurs
    """
    #Regarder si l'une des entrée est vide
    if username == "" or password == "":
        raise WrongFormat
    
    #Essayer d'enregistrer un utilisateur
    req = Wb.web_client.post("https://api.nsi.quark-dev.com/users", {"username":username,"password":password})
    
    #Regarder pour des erreurs
    if req.text == "user already exist !":
        raise UserAlreadyExist
    
    if req.text == "user sucessfully added !":
        return User(username)
    else:
        raise UnknownResponse

    
    
        
        
