import sqlite3

if __name__ == '__main__':
    con=sqlite3.connect('librachain')
    cur=con.cursor()
    cur.execute("DROP TABLE IF EXISTS Users");
    cur.execute("DROP TABLE IF EXISTS SmartContracts");
    cur.execute("""
        CREATE TABLE Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            public_key TEST NOT NULL,
            private_key TEST NOT NULL,
            password_edit_timestamp TEXT NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE SmartContracts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            shard INTEGER NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES Users (id),
            UNIQUE(address, shard)
        );
    """)
    con.commit()
    con.close()
