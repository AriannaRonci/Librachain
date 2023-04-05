import os
import sqlite3
import base64
import hashlib
from cryptography.fernet import Fernet
from models.user import User
from config import config

class UserRepository:
    def __init__(self):
        self.conn = sqlite3.connect(config.config["db_path"])
        self.cursor = self.conn.cursor()
        self._create_table_if_not_exists()

        # Parameters for password hashing
        self.n=2
        self.r=16
        self.p=1
        self.dklen=64
    
    def _create_table_if_not_exists(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                public_key TEXT NOT NULL,
                private_key TEXT NOT NULL )
        """)

    def check_password(self, username, password):
        res = self.cursor.execute("SELECT password_hash FROM Users WHERE username = ?", (username,))
        c = res.fetchone()
        if c:
            stored_pw = c[0]
            parameters = stored_pw.split('$')
            hashed_password = hashlib.scrypt(
                password.encode('utf-8'),
                salt=bytes.fromhex(parameters[1]),
                n=int(parameters[2]),
                r=int(parameters[3]),
                p=int(parameters[4]),
                dklen=int(parameters[5])
            ) 
            if hashed_password.hex() == parameters[0]:
                return True
            else:
                return False
        else:
            return False

    def get_user_by_username(self, username):
        user = None
        res = self.cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
        if res is None:
            return None
        else:
            tuple = res.fetchone()
            user = User(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4])
            return user

    def register_user(self, username, password, public_key, private_key):
        try:
            self.cursor.execute(f"INSERT INTO Users (username, password_hash, public_key, private_key) VALUES (?, ?, ?, ?)", (username, self.hash_password(password), public_key, private_key))
            self.conn.commit()
            return True
        except Exception as err:
            print(err)
            return False
    def hash_password(self, password):
        salt = os.urandom(10)
        hash = hashlib.scrypt(password.encode(), salt=salt, n=self.n, r=self.r, p=self.p, dklen=self.dklen)
        password_hash = f"{hash.hex()}${salt.hex()}${self.n}${self.r}${self.p}${self.dklen}"
        return password_hash

    def encrypt_private_key(self, private_key, password):
        password_hash = hashlib.sha256(password.encode('utf-8')).digest()
        key = base64.urlsafe_b64encode(password_hash.encode("utf-8"))
        cipher_suite = Fernet(key)
        encrypted_private_key = cipher_suite.encrypt(private_key.encode('utf-8'))
        return encrypted_private_key

    def decrypt_private_key(self, encrypted_private_key, password):
        password_hash = hashlib.sha256(password.encode('utf-8')).digest()
        key = base64.urlsafe_b64encode(password_hash.encode('utf-8'))
        cipher_suite = Fernet(key)
        private_key = cipher_suite.decrypt(encrypted_private_key.encode('utf-8'))
        return private_key

    def delete_user(self, user):
        self.cursor.execute("DELETE FROM Users WHERE id=?",(user.get_id()))
        self.con.commit()

    def getLatestTimestamp():
        res = self.cursor.execute("SELECT * FROM Users WHERE username=?", (username,))

    def setLatestTimestamp():
        pass

