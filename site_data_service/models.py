from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
  pass


class MDFile(Base):
  __tablename__ = 'md_files'

  id: Mapped[int] = mapped_column(primary_key=True)
  file_path: Mapped[str] = mapped_column(sa.String(255), nullable=False)
  mod_time: Mapped[datetime] = mapped_column(
    sa.DateTime(timezone=True), server_default=func.now(), nullable=False
  )
  page: Mapped['Page'] = relationship(back_populates='md_file')


class Page(Base):
  __tablename__ = 'pages'

  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str] = mapped_column(sa.String(255), nullable=False)
  draft: Mapped[bool] = mapped_column(sa.Boolean, nullable=False)
  type: Mapped[str] = mapped_column(sa.String(10), nullable=False)
  published: Mapped[datetime] = mapped_column(
    sa.DateTime(timezone=True), server_default=None, nullable=True
  )
  content: Mapped[str] = mapped_column(sa.VARCHAR)
  relative_path: Mapped[str] = mapped_column(sa.String(255), nullable=False)
  md_file_id: Mapped[int] = mapped_column(sa.ForeignKey('md_files.id'))
  md_file: Mapped['MDFile'] = relationship(back_populates='page')


# # class Photo(Base):
# #   __tablename__ = 'photos'
# #
# #   id: Mapped[int] = mapped_column(primary_key=True)
# #   url: Mapped[int] = mapped_column(nullable=False)
# #
# #
# # class PhotoDetail(Base):
# #   __table_name__ = 'photo_details'
# #   id: Mapped[int] = mapped_column(db.ForeignKey('photos.id'))
# #   key: Mapped[str] = mapped_column(db.String(255))
# #   value: Mapped[str] = mapped_column(db.String(255))
# #
# #   __table_args__ = (
# #     db.UniqueConstraint(id, key)
# #   )