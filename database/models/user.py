# user.py
from sqlalchemy import Table, Column, BigInteger, ForeignKey, String, insert, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.base import CreatedModel, db, AbstractClass

# User-Categories Association Table
user_categories = Table(
    'user_categories',
    CreatedModel.metadata,
    Column('user_id', BigInteger, ForeignKey('users.id'), primary_key=True),
    Column('category_id', BigInteger, ForeignKey('categories.id'), primary_key=True)
)

# User-Sites Association Table
user_sites = Table(
    'user_sites',
    CreatedModel.metadata,
    Column('user_id', BigInteger, ForeignKey('users.id'), primary_key=True),
    Column('site_id', BigInteger, ForeignKey('sites.id'), primary_key=True)
)

# User-Channels Association Table
user_channels = Table(
    'user_channels',
    CreatedModel.metadata,
    Column('user_id', BigInteger, ForeignKey('users.id'), primary_key=True),
    Column('channel_id', BigInteger, ForeignKey('channels.id'), primary_key=True)
)


class User(CreatedModel):
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    language: Mapped[str] = mapped_column(String, default='uz')

    categories: Mapped[list['Category']] = relationship('Category', secondary=user_categories, back_populates="users")
    sites: Mapped[list['Site']] = relationship('Site', secondary=user_sites, back_populates='users')
    channels: Mapped[list['Channel']] = relationship('Channel', secondary=user_channels, back_populates='users')

    async def get_categories(self):
        from database.models import Category
        query = select(Category).join(user_categories).where(user_categories.c.user_id == self.id)
        result = await db.execute(query)
        return list(result.scalars())

    async def add_user_categories(self, category_ids: list[int]):
        if not category_ids:
            return

        values_to_insert = [{'user_id': self.id, 'category_id': category_id} for category_id in category_ids]
        stmt = insert(user_categories).values(values_to_insert)
        await db.execute(stmt)
        await AbstractClass.commit()

    async def get_sites(self):
        from database.models import Site
        query = select(Site).join(user_sites).where(user_sites.c.user_id == self.id)
        result = await db.execute(query)
        return list(result.scalars())

    async def add_user_sites(self, site_ids: list[int]):
        if not site_ids:
            return

        values_to_insert = [{'user_id': self.id, 'site_id': site_id} for site_id in site_ids]
        stmt = pg_insert(user_sites).values(values_to_insert).on_conflict_do_nothing()
        await db.execute(stmt)
        await db.commit()

    async def get_user_channels(self):
        from database.models import Channel
        query = select(Channel).join(user_channels).where(user_channels.c.user_id == self.id)
        result = await db.execute(query)
        return list(result.scalars())

    async def add_user_channels(self, channel_ids):
        if not channel_ids:
            return

        values_to_insert = [{'user_id': self.id, 'channel_id': channel_id} for channel_id in channel_ids]
        stmt = insert(user_channels).values(values_to_insert)
        await db.execute(stmt)
        await AbstractClass.commit()

    def __repr__(self) -> str:
        return f"<User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, username={self.username})>"
