import os
import time
import sqlite3
import base64
import hashlib
from cryptography.fernet import Fernet
from models.smart_contract import SmartContract
from models.user import User
from config import config


class UserRepository:
    """User Data Access Layer to access the database.
    Attributes:
        conn: Connection object representing the connection to the SQLite DB
        cursor: Cursor object to execute operations on the DB
        n_param:  Integer memory/cpu factor for the password hashing algorithm
        r_param: Integer block size for the password hashing algorithm
        p_param: parallelization factor for the password hashing algorithm
        dklen_param: length of the derived key from password the hashing algorithm
    """

    def __init__(self):
        """Initializes the class and the db Connection and Cursor object.

        Connection object is created with the database present in the
        path contained in config.config["db_path"].
        The _create_table_if_not_exists method is called to ensure the
        User table exists.
        """
        self.conn = sqlite3.connect(config.config["db_path"])
        self.cursor = self.conn.cursor()
        self._create_table_if_not_exists()

        # Parameters for password hashing
        self.n_param = 2
        self.r_param = 16
        self.p_param = 1
        self.dklen_param = 64

        # 3 months in seconds
        self.pw_obsolescence_time = 60*60*24*30

    def _create_table_if_not_exists(self):
        """Creates the user table in the db if it doesn't exist already"""

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                public_key TEXT NOT NULL,
                private_key TEXT NOT NULL,
                password_edit_timestamp TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS SmartContracts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                shard INTEGER NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES Users (id),
                UNIQUE(address, shard)
            )
        """)
        self.conn.commit()

    def check_password(self, username, password):
        """Checks that the given credentials are valid.
        Password hash recovered from the database and compared to
        supplied password digest. If a user with the supplied username
        exists in the database and the corresponding password hash
        matches the digest of the supplied password than the credentials
        are valid.
        Args:
            ursername: username string
            password: password string
        Returns:
            A boolean that identifies the result:
            - True: supplied credentials are valid
            - False: supplied credentials are not valid
        """
        res = self.cursor.execute("""
        SELECT password_hash 
        FROM Users 
        WHERE username = ?""", (username,)
                                  )
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
            return hashed_password.hex() == parameters[0]

        return False

    def get_user_by_username(self, username):
        """Retrieves user with supplied username from database.
        Args:
            username: username string
        Returns:
            A User object if a match is found in the database, None otherwise.
        """
        res = self.cursor.execute("""
            SELECT *
            FROM Users 
            WHERE username=?""", (username,))
        if res is not None:
            user_attr = res.fetchone()
            deployed_smart_contracts = self.get_user_smart_contracts(user_attr[0])
            user = User(user_attr[0], user_attr[1], user_attr[2],
                        user_attr[3],user_attr[4], deployed_smart_contracts)
            return user

        return None

    def register_user(self, username, password, public_key, private_key):
        """Inserts a new User record in the database.
        The private key is encrypted using password as seed, and
        password is hashed upon insertion.
        Args:
            username: user's username string
            password: user's password string
            public_key: user's public key string
            private_key: user's private key string
        Returns:
            An integer the identifies the result:
                 0: insertion done correctly
                -1: supplied username already present in the database
                -2: uknown database error
        """
        try:
            encrypted_private_key = self.encrypt_private_key(
                private_key, password)
            hashed_password = self.hash_password(password)
            self.cursor.execute("""
                INSERT INTO Users
                (username, password_hash, public_key, private_key, password_edit_timestamp)
                VALUES (?, ?, ?, ?, ?)""",
                (username, hashed_password, public_key, encrypted_private_key, str(time.time()))
                                )
            self.conn.commit()
            return 0
        except sqlite3.IntegrityError:
            return -1
        except sqlite3.DatabaseError:
            return -2

    def hash_password(self, password: str):
        """Hashes the supplied password.
        The parameters used by scrypt algorithm are appended to the digest
        and returned.
        Args:
            password: supplied password string
        Returns:
            A string containing the hashed password and the parameters used
            to hash it.

        """
        salt = os.urandom(10)
        digest = hashlib.scrypt(
            password.encode(), salt=salt,
            n=self.n_param,
            r=self.r_param,
            p=self.p_param,
            dklen=self.dklen_param
        )
        password_hash = f"{digest.hex()}${salt.hex()}${self.n_param}${self.r_param}${self.p_param}${self.dklen_param}"
        return password_hash

    def encrypt_private_key(self, private_key: str, password: str):
        """Encrypts the supplied private key.
        The password is hashed with sha256 and used as key for the private key
        encryption.
        Args:
            private_key: private key string
            password: password string
        Returns:
            a string containing encrypted private key.
        """
        password_hash = hashlib.sha256(password.encode('utf-8')).digest()
        key = base64.urlsafe_b64encode(password_hash)
        cipher_suite = Fernet(key)
        encrypted_private_key = cipher_suite.encrypt(
            private_key.encode('utf-8'))
        return encrypted_private_key

    def decrypt_private_key(self, encrypted_private_key, password):
        """Decrypts the supplied private key.
        The password is hashed with sha256 and used as key for the private key
        decryption.
        Args:
            encrypted_private_key: encrypt_private_key key string
            password: password string
        Returns:
            A string containing the decrypted private key.
        """
        password_hash = hashlib.sha256(password.encode('utf-8')).digest()
        key = base64.urlsafe_b64encode(password_hash)
        cipher_suite = Fernet(key)
        private_key = cipher_suite.decrypt(
            encrypted_private_key.encode('utf-8'))
        return private_key.decode('utf-8')

    def delete_user(self, user):
        """Deletes the supplied user from the database.
        Args:
            user: User object which database entry has to be deleted
        Returns:
            An integer that identifies the result:
                  0: user deleted correctly
                 -1: unknown database error
        """
        try:
            self.cursor.execute("DELETE FROM Users WHERE id=?", (user.get_id(),))
            self.conn.commit()
            return 0
        except:
            return -1

    def get_user_smart_contracts(self, user_id: int):
        """Retrives the list of smart contracts deployed by a user.
        Args:
            user_id: Integer, user's id
        Returns:
            the list of smart contracts
        Raises:
            Many types of possible exceptions, not yet specified
        """
        try:
            res = self.cursor.execute("SELECT * FROM SmartContracts WHERE user_id=?", (user_id,)).fetchall()
            smart_contracts = [SmartContract(row[1], row[2], row[3], row[4], row[0]) for row in res]
            return smart_contracts
        except Exception as ex:
            raise ex

    def get_smart_contract_by_address(self, address, shard):
        try:
            row = self.cursor.execute("SELECT * FROM SmartContracts WHERE shard=? and address=?",
                                      (shard, address)).fetchone()
            smart_contracts = SmartContract(row[1], row[2], row[3], row[4], row[0])
            return smart_contracts
        except Exception as ex:
            raise ex

    def insert_deployed_smart_contract(self, smart_contract: SmartContract):
        """Inserts smart contract entry in database.
        Args:
            smart_contract:
        Returns:
            An integer that identifies the result:
                  0: user deleted correctly
                 -1: invalid entry
                 -2: unknown database error
        """
        try:
            self.cursor.execute("""
                    INSERT INTO SmartContracts
                    (name, address, shard, user_id)
                    VALUES (?, ?, ?, ?)""",
                                (smart_contract.get_name(),
                                 smart_contract.get_address(),
                                 smart_contract.get_shard(),
                                 smart_contract.get_user_id())
                                )
            self.conn.commit()
            return 0
        except sqlite3.OperationalError:
            return -1
        except Exception:
            return -2

    def delete_deployed_smart_contract(self, smart_contract: SmartContract):
        try:
            self.cursor.execute("DELETE FROM SmartContracts WHERE id=?", (smart_contract.get_id(),))
            self.conn.commit()
            return 0
        except sqlite3.OperationalError:
            return -1
        except Exception:
            return -2

    def change_password(self, username, new_password, old_password):
        """Change user password in db.

        The private key ciphertext is recalculated again using the new password.
        Record's password_edit_timestamp is updated to current timestamp.

        Args:
            username: 
            new_password:
            old_password:
        Returns:
             0: succesfully changed password
            -1: user entry not found in db
        Raises:
            The exception raised by the db when runnin the query

        TODO: missing args
        """

        user = self.get_user_by_username(username)
        if user is not None:
            password_hash = self.hash_password(new_password)
            private_key = self.decrypt_private_key(user.get_private_key(), old_password)
            encrypted_private_key = self.encrypt_private_key(private_key, new_password)

            try:
                self.cursor.execute("""
                    UPDATE Users
                    SET password_hash = ?, private_key = ?, password_edit_timestamp = ?
                    WHERE username = ?""",
                    (password_hash, encrypted_private_key, username, str(int(time.time())))
                )
                self.conn.commit()
                return 0
            except Exception as ex:
                raise ex
        else:
            return -1

    def is_password_obsolete(self, username):
        try:
            password_edit_timestamp = int(self.cursor.execute("""
                SELECT password_edit_timestamp FROM Users
                WHERE username = ?""", (username,)).fetchone()[0])

            if int(time.time()) - password_edit_timestamp >= self.pw_obsolescence_time:
                return True
            return False
        except Exception as ex:
            raise ex

    def check_keys(self, username, password, public_key, private_key):
        user = self.get_user_by_username(username)
        if (
            user is not None and self.check_password(username, password) and
            user.get_public_key() == public_key and
            user.get_private_key() == self.encrypt_private_key(private_key, password)
        ):
            return True
        else:
            return False

    # def get_latest_timestamp(self):
    #    pass

    # def set_latest_timestamp(self):
    #    pass
