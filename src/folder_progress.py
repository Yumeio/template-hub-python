import os

class FolderProgress():
    path_token = os.path.expanduser("~/.test-hub/token");
    
    @classmethod
    def add_token(cls, token: str) -> None:
        os.makedirs(os.path.dirname(cls.path_token), exist_ok=True)
        with open(cls.path_token, "w") as f:
            f.write(token)
        
    @classmethod
    def get_token(cls) -> str:
        try:
            with open(cls.path_token, "r") as f:
                return f.read()
        except FileNotFoundError:
            raise Exception("Token not found")
    
    @classmethod
    def remove_token(cls) -> None:
        try:
            os.remove(cls.path_token)
        except FileNotFoundError:
            pass