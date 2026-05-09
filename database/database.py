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
                url TEXT NOT NULL UNIQUE
            )
         """)
         cur.execute("PRAGMA journal_mode=WAL")
         cur.execute("""
            CREATE TABLE IF NOT EXISTS chapters(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                volume INTEGER UNIQUE,
                chapter INTEGER UNIQUE,
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

    def add_chapter(self, book_id: int, volume: int, chapter: int, text: str, rule: int = None) -> None:
        cur = self.cursor
        cur.execute("""
            INSERT INTO chapters (book_id, volume, chapter, rule, text)
            VALUES (?, ?, ?, ?, ?)
        """, (book_id, volume, chapter, rule, text)
                    )
        self.connect.commit()

    def get_book(self, title: str) -> int:
        cur = self.cursor
        cur.execute(
            "SELECT * FROM books WHERE title = ?",
            (title,)
        )
        return cur.fetchone()['id']

    def get_chapters_by_book_id(self, book_id: int, volume: int, chapter: int) -> str:
        cur = self.cursor
        cur.execute(
            "SELECT * FROM chapters WHERE book_id = ? AND volume = ? AND chapter = ?",
            (book_id, volume, chapter)
        )
        return cur.fetchone()['text']

    def conn_close(self):
        self.cursor.close()
        self.connect.close()

if __name__ == '__main__':
    db = MyBase('../data.sql')
    id = db.get_book(title='освободите эту ведьму')
    print(db.get_chapters_by_book_id(book_id=id, volume=1, chapter=1000))
    db.conn_close()