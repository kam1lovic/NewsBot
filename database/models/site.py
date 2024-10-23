# site.py
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.base import CreatedModel, db


class Site(CreatedModel):
    url: Mapped[str] = mapped_column(String, unique=True)

    users: Mapped[list['User']] = relationship('User', secondary='user_sites', back_populates='sites')

    def __repr__(self) -> str:
        return f"<Site(id={self.id}, url={self.url})>"

    @classmethod
    async def get_site_by_url(cls, url: str):
        query = select(cls).where(cls.url == url)
        result = await db.execute(query)
        site = result.scalar_one_or_none()
        return site

    @classmethod
    async def create(cls, url: str):
        site = cls(url=url)
        db.add(site)
        await db.commit()
        return site
