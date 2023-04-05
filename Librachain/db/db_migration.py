import sqlite3

if __name__ == '__main__':
    con=sqlite3.connect('librachain')
    cur=con.cursor()
    cur.execute('''
        CREATE TABLE Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        public_key TEST NOT NULL,
        private_key TEST NOT NULL
        );

        CREATE TABLE Timestamps(
            
        );
    ''')
    con.commit()
    con.close()
