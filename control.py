import sqlite3

class Database:
    def __init__(self, path="work.db"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._init()

    def _init(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS works(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            is_done INTEGER DEFAULT 0
                            )""")
        
    def add(self, title: str, is_done:int):
        self.cursor.execute("INSERT INTO works (title, is_done) VALUES (?,?)",
                            (title, is_done))
        self.conn.commit()
    
    def delete(self, work_id:int):
        self.cursor.execute("DELETE FROM works WHERE id=?",(work_id,))
        self.conn.commit()

    def get_all(self):
        self.cursor.execute("SELECT * FROM works")
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()
