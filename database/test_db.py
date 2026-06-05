import asyncio

from sqlalchemy import select, and_

from sqlalchemy.orm import selectinload

from models import Book, Chapter

from session import SessionLocal, create_db

async def add_book(session, title: str, url: str):
    book = Book(title=title, url=url)
    session.add(book)
    await session.commit()
    return book.id

async def add_chapter(session, book_id: int, volume: int, chapter: int, text: str):
    chapter = Chapter(book_id=book_id, volume=volume,chapter=chapter,text=text)
    session.add(chapter)
    await session.commit()

async def get_book(session, title: str):
    stm = select(Book).where(Book.title == title)
    result = await session.execute(stm)
    return result.scalar_one_or_none()

async def get_chapter(session, book_id: int, volume: int, chapter: int):
    stm = (select(Chapter).where(and_(Chapter.book_id == book_id, Chapter.volume == volume, Chapter.chapter == chapter)))
    result = await session.execute(stm)
    return result.scalar_one_or_none()


async def main():
    await create_db()

    # async with SessionLocal() as session:
    #     book_id = await add_book(session, title="Witche", url="lalala")
    #
    # async with SessionLocal() as session:
    #     await add_chapter(session, book_id=book_id, volume=1, chapter=1, text="Сегодня был прекрасный день, солнышко не светило")

    async with SessionLocal() as session:
        book = await get_book(session=session, title="Witches")
        print(book)
        chapter = await get_chapter(session, book.id, 1, 1)
        print(chapter)


if __name__ == "__main__":
    asyncio.run(main())
