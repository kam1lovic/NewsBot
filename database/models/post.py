from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.base import CreatedModel


class Post(CreatedModel):
    post_link: Mapped[str] = mapped_column(String, unique=True)
    content: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self) -> str:
        return f"<Post(id={self.id}, post_link={self.post_link})>"


class SummarizedPost(CreatedModel):
    content_uz: Mapped[str] = mapped_column(String)
    content_en: Mapped[str] = mapped_column(String)
    content_ru: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped['Category'] = relationship('Category', back_populates='posts')
    post_link: Mapped[str] = mapped_column(String)
    sent: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<SummarizedPost(id={self.id}, content={self.content_uz})>"
