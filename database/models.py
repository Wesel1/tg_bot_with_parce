from sqlalchemy import ForeignKey, UniqueConstraint

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    url: Mapped[str] = mapped_column(unique=True)

    def __repr__(self):
        return f"Book(id={self.id}, title='{self.title}')"


class Chapter(Base):
    __tablename__ = "chapters"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    volume: Mapped[int]
    chapter: Mapped[int]
    rule: Mapped[int | None]
    text: Mapped[str]

    __table_args__ = (UniqueConstraint("book_id", "volume", "chapter"),)

    def __repr__(self):
        return (
            f"Chapter("
            f"volume={self.volume}, "
            f"chapter={self.chapter}"
            f")"
        )