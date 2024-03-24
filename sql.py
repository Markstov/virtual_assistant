import sqlite3

class DBManager:

    def __init__(self):
        self.conn = sqlite3.connect('software.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS programs(
            programid INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            name TEXT,
            path TEXT,
            alias TEXT DEFAULT '');
            """)
        self.conn.commit()

    def insert_data(self, app_name, exe_path):
        self.cursor.execute(f"INSERT INTO programs(name, path) VALUES(?, ?);", [app_name, exe_path])
        self.conn.commit()

    def is_exist_by_name(self, name):
        self.cursor.execute(f"SELECT * FROM programs WHERE name=?", [name])
        if self.cursor.fetchall():
            return True
        else:
            return False
        
    def all_programs(self):
        self.cursor.execute(f"SELECT * FROM programs")
        return self.cursor.fetchall()
    
    def data_for_gui(self):
        self.cursor.execute(f"SELECT name, path, alias FROM programs")
        data = (row for row in self.cursor.fetchall())
        print(data)
        return data
        
if __name__ == "__main__":
    db = DBManager()
    # print(db.is_exist_by_name("Don't Starve Together"))
    print(len(db.all_programs()))

