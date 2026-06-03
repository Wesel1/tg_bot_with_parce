import asyncio
import aiosqlite as sq


class MyBase:
    def __init__(self, path: str):
        self.path = path
        self.connect = None

    async def setup(self):
        self.connect = await sq.connect(self.path)
        self.connect.row_factory = sq.Row

    async def create_tables(self):
        async with self.connect.cursor() as cur:
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    
                    UNIQUE(title, url)
                )
             """)
            await cur.execute("PRAGMA journal_mode=WAL")
            # await cur.execute("PRAGMA foreign_keys = ON")
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS chapters(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER,
                    volume INTEGER,
                    chapter INTEGER,
                    rule INTEGER,
                    text TEXT,
                    
                    UNIQUE(volume, chapter)
                    
                    FOREIGN KEY(book_id) REFERENCES books(id)
                )
             """)
            await self.connect.commit()

    async def add_book(self, title: str, url: str) -> int:
        async with self.connect.cursor() as cur:
            await cur.execute(
                "INSERT INTO books (title, url) VALUES (?, ?) ", (title, url)
            )
            await self.connect.commit()
            return cur.lastrowid

    async def add_chapter(
        self, book_id: int, volume: int, chapter: int, text: str, rule: int = None
    ) -> None:
        async with self.connect.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO chapters (book_id, volume, chapter, rule, text)
                VALUES (?, ?, ?, ?, ?)
            """,
                (book_id, volume, chapter, rule, text),
            )
            await self.connect.commit()

    async def get_book(self, title: str):
        async with self.connect.cursor() as cur:
            await cur.execute("SELECT id, url FROM books WHERE title = ?", (title,))
            return await cur.fetchone()

    async def get_chapters_by_book_id(self, book_id: int, volume: int, chapter: int):
        async with self.connect.cursor() as cur:
            await cur.execute(
                "SELECT * FROM chapters WHERE book_id = ? AND volume = ? AND chapter = ?",
                (book_id, volume, chapter),
            )
            return await cur.fetchone()

    async def close(self):
        await self.connect.close()


async def main():
    db = MyBase("data.sql")
    await db.setup()
    await db.create_tables()

    # id = await db.add_book('освободите эту ведьму', "https://ranobelib.me")
    # await db.add_chapter(id, 1, 1, "Я приехал жить в Лондон")
    # await db.add_chapter(id, 1, 2, "Я приехал жить в Махачкалу")
    # await db.add_chapter(id, 1, 3, "Я приехал жить в Испанию")
    # await db.add_chapter(id, 1, 4, "Я приехал жить в Монако")

    book = await db.get_book(title="освободите эту ведьму")
    # print(f"{book['id']}, {book['title']}, {book['url']}")
    book_id, url = book
    print(book_id, url)

    a = await db.get_chapters_by_book_id(book_id, 1, 4)
    print(a["text"])
    # print(db.get_chapters_by_book_id(book_id=book['id'], volume=1, chapter=1000))
    await db.close()


if __name__ == "__main__":
    asyncio.run(main())
