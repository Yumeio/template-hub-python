import os, requests
from os.path import expanduser
from typing import Dict, List, Optional, Tuple

class Repository():
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class FolderProgress():
    path_token = expanduser("~/.test-hub/token");
    
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

obj = Repository(name="my-repo", owner="my-owner")
print(obj.name)