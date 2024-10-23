# channel.py
from sqlalchemy import Column, String, select
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.base import CreatedModel, db


class Channel(CreatedModel):
    name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, unique=True)

    users: Mapped[list['User']] = relationship('User', secondary='user_channels', back_populates='channels')

    def __repr__(self) -> str:
        return f"<Channel(id={self.id}, name={self.name}, username={self.username})>"

    @classmethod
    async def get_channels_by_username(cls, username: str):
        query = select(cls).join(cls.users).where(cls.username == username)
        result = await db.execute(query)
        channels = result.scalars().all()
        return channels
