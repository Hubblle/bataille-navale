"""
Le module du client web

Description:
    Ce module est utilisé pour faire des requêtes à l'api avec une gestion automatique des cookies stockés localement, avec chargement automatique au démarrage du programme !


"""

#Imports
from requests import Session
from requests.cookies import RequestsCookieJar
import os
import json



#### Basics
def open_json(path:str) -> dict|None:
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_json(data:dict, path:str) -> None:
    with open(path, "w") as f:
        return json.dump(data, f, indent=4)
    


def get_last_cookies() -> RequestsCookieJar:
    """
    Une fonction qui renvoie les derniers cookies stockés localement
    
    Returns:
        RequestsCookieJar: L'objet des cookies
    """
    
    cookies = RequestsCookieJar()
    cookie_path = os.path.join(os.path.dirname(__file__), "cache/jar.json")
    
    if os.path.exists(cookie_path):

        #Récupérer le json et l'importer
        for key, value in open_json(cookie_path).items():
                cookies.set(key, value)
                
    return cookies
    
    
    
def save_cookies(cookies:RequestsCookieJar):
    """
    Fonction qui sauvegarde localement les cookies dans un fichier json
    
    """
    
    cookies_dict = cookies.get_dict()
    cookie_path = os.path.join(os.path.dirname(__file__), "cache/jar.json")
    
    save_json(cookies_dict, cookie_path)



class Web_client():
    """La classe du client web
    """
    def __init__(self):
        self.session = Session()

        
        # Recupérer les derniers cookies
        self.session.cookies = get_last_cookies()
    
    def save_current_cookies(self):
        """
        A func which save currents cookies for later use
        """
        
        save_cookies(self.session.cookies)
        
    
    #Methods override
    def get(self, *args, **kwargs):
        """
        Override get method pour sauvegarder les cookies automatiquement
        """

        response = self.session.get(*args, **kwargs)

        self.save_current_cookies()
        return response
    
    def post(self, *args, **kwargs):
        """
        Override post method pour sauvegarder les cookies automatiquement
        """
        response = self.session.post(*args, **kwargs)
        self.save_current_cookies()
        return response
        
    def delete(self, *args, **kwargs):
        """
        Override delete method pour sauvegarder les cookies automatiquement
        """
        response = self.session.delete(*args, **kwargs)
        self.save_current_cookies()
        return response
        
    
    

# Créer le client web
web_client = Web_client()