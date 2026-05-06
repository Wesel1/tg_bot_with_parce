import sqlite3

class MyBase:
    def __init__(self, path: str):
        self.connect = sqlite3.connect(path)
        self.connect.row_factory = sqlite3.Row
        self.cursor = self.connect.cursor()

    def create_tables(self):
         cur = self.cursor
         cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                url TEXT
            )
         """)
         cur.execute("PRAGMA journal_mode=WAL")
         cur.execute("""
            CREATE TABLE IF NOT EXISTS chapters(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                volume INTEGER,
                chapter INTEGER,
                rule INTEGER,
                text TEXT,
                FOREIGN KEY(book_id) REFERENCES books(id)
            )
         """)
         self.connect.commit()


    def add_book(self, title: str, url: str) -> int:
        cur = self.cursor
        cur.execute(
            "INSERT INTO books (title, url) VALUES (?, ?) ",
            (title, url)
        )
        self.connect.commit()
        return cur.lastrowid

    def add_chapter(self, book_id: int, volume: int, chapter: int, rule: int, text: int):
        cur = self.cursor
        cur.execute("""
            INSERT INTO chapters (book_id, volume, chapter, rule, text)
            VALUES (?, ?, ?, ?, ?)
        """, (book_id, volume, chapter, rule, text)
                    )
        self.connect.commit()

    def get_book(self, title: str):
        cur = self.cursor
        cur.execute(
            "SELECT * FROM books WHERE title = ?",
            (title,)
        )
        return cur.fetchone()

    def get_chapters_by_book_id(self, book_id: int):
        cur = self.cursor
        cur.execute(
            "SELECT * FROM chapters WHERE book_id = ?",
            (book_id,)
        )
        return cur.fetchall()


    def conn_close(self):
        self.cursor.close()
        self.connect.close()

if __name__ == '__main__':
    db = MyBase('help.sql')