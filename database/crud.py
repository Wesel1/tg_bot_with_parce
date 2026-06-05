from sqlalchemy import select, and_

from sqlalchemy.orm import selectinload

from database.models import Book, Chapter

from database.session import SessionLocal

async def add_book(title: str, url: str):
    async with SessionLocal() as session:
        book = Book(title=title, url=url)
        session.add(book)
        await session.commit()
        return book.id

async def add_chapter(book_id: int, volume: int, chapter: int, text: str):
    async with SessionLocal() as session:
        chapter = Chapter(book_id=book_id, volume=volume,chapter=chapter,text=text)
        session.add(chapter)
        await session.commit()

async def get_book(title: str):
    async with SessionLocal() as session:
        stm = select(Book).where(Book.title == title)
        result = await session.execute(stm)
        return result.scalar_one_or_none()

async def get_chapter(book_id: int, volume: int, chapter: int):
    async with SessionLocal() as session:
        stm = (
            select(Chapter).where(
                and_(
                    Chapter.book_id == book_id,
                    Chapter.volume == volume,
                    Chapter.chapter == chapter
                )
            )
        )
        result = await session.execute(stm)
        return result.scalar_one_or_none()
