import re
import hashlib

import flask

from .GlobalController import GlobalController

class AuthController(GlobalController):
    def __init__(self) -> None:
        super().__init__()
    def register(self, data):
        username = data.get("username")
        lastname = data.get("lastname")
        surname = data.get("surname")
        account_num = data.get("account")
        password = data.get("password")
        # checks the correctness of the data
        if not re.match("[0-9]+", account_num) or not username or not lastname or not surname or not password:
            return -1
        if self.database.pull_from_db("SELECT id FROM users WHERE username = %s OR lastname = %s OR firstname = %s OR account_num = %s", (username, lastname, surname, account_num), only_first=True) is not None:
            return -1
        hashed_pswd = self.utils.hash_password(password)
        params = (lastname, surname, username, account_num, hashed_pswd)
        user_id = 0
        if self.database.save_to_db("INSERT INTO users (lastname, firstname, username, account_num, password, register_date) VALUES (%s, %s, %s, %s, %s, NOW());", params):
            user_id = self.database.pull_from_db("SELECT id FROM users WHERE username = %s;", params=(username,), only_first=True)[0]
        return user_id
    
    def login(self, data):
        username = data.get("username")
        password = data.get("password")
        entered_password = self.utils.hash_password(password)

        db_user = self.database.pull_from_db("SELECT * FROM users WHERE username = %s AND password = %s", params=(username, entered_password), only_first=True)
        if db_user is None:
            return -1
        
        return db_user[0]

        
