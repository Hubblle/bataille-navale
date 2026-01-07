"""
Le module qui contient toutes les Exceptions du module
"""

class UserDontExist(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        
class WrongCredentials(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        
class UnknownResponse(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        
class WrongFormat(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        
class UserAlreadyExist(Exception):
    def __init__(self, *args):
        super().__init__(*args)