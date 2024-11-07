from sqlalchemy import String

from database.base import CreatedModel
from sqlalchemy.orm import Mapped, mapped_column


class Organization(CreatedModel):
    name_uz: Mapped[str] = mapped_column(String)
    name_en: Mapped[str] = mapped_column(String)
    name_ru: Mapped[str] = mapped_column(String)
    original_name: Mapped[str] = mapped_column(String)
    latin_name: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    type_uz: Mapped[str] = mapped_column(String)
    type_en: Mapped[str] = mapped_column(String)
    type_ru: Mapped[str] = mapped_column(String)
