import sqlite3

class HelpBase:
    def __init__(self, path: str):
        self.path = path
        self.create_base()

    def create_base(self):
         with sqlite3.connect(self.path) as m:
             cursor = m.cursor()
             cursor.execute("CREATE TABLE IF NOT EXISTS catalogue (id INTEGER PRIMARY KEY, status TEXT, data_from_site TEXT);")
             cursor.execute("PRAGMA journal_mode=WAL")


    def save(self, status: str, text: str):
        with sqlite3.connect(self.path) as a:
            cursor = a.cursor()
            cursor.execute(
                "INSERT INTO catalogue (id, status, data_from_site) VALUES (1, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET "
                "status = excluded.status, "
                "data_from_site = excluded.data_from_site",
                (status, text)
            )

    def find(self, status):
        with sqlite3.connect(self.path) as b:
            cursor = b.cursor()
            cursor.execute(
                "SELECT status, data_from_site FROM catalogue WHERE status = ?", (f"{status}",)
            )
            return cursor.fetchone()


    def delete(self):
        with sqlite3.connect(self.path) as c:
            cursor = c.cursor()
            cursor.execute("DELETE FROM catalogue WHERE id = 1")

if __name__ == '__main__':
    db = HelpBase('help.db')
    db.delete()
    db.save('parce_done', 'Ну допустим')
    print(db.find('parce_done'))