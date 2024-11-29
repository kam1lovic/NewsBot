# category.py
from sqlalchemy import String, BigInteger, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.base import CreatedModel
from database.models import User


class Category(CreatedModel):
    name: Mapped[str] = mapped_column(String, unique=True)
    name_uz: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    name_ru: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    emoji: Mapped[str] = mapped_column(String)

    users: Mapped[list['User']] = relationship('User', secondary='user_categories', back_populates='categories')
    posts: Mapped[list['SummarizedPost']] = relationship('SummarizedPost', back_populates='category')
    dynamic_category: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name={self.name})>"
