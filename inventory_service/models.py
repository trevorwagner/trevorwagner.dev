import datetime, json

from typing import List

import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from pathlib import Path


class Base(DeclarativeBase):
  def __enter__(self):
    pass
  def __exit__(self, exc_type, exc_val, exc_tb):
    pass
  def __getitem__(self, index):
    pass


class MDFile(Base):
  __tablename__ = 'md_files'

  id: Mapped[int] = mapped_column(primary_key=True)
  _file_path: Mapped[str] = mapped_column(sa.String(255))
  mod_time: Mapped[datetime.datetime] = mapped_column(
    sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
  )
  _page_metadata: Mapped[str] = mapped_column(sa.VARCHAR)
  page_content: Mapped[str] = mapped_column(sa.VARCHAR)

  page: Mapped['Page'] = relationship(back_populates='md_file')

  @hybrid_property
  def file_path(self):
    return Path(str(self._file_path))
  
  @file_path.setter
  def file_path(self, path: Path):
    self._file_path = str(path)

  @hybrid_property
  def page_metadata(self):
    return json.loads(str(self._page_metadata))

  @page_metadata.setter
  def page_metadata(self, dict):
    self._page_metadata = json.dumps(dict)
  
  def __repr__(self):
    return f"<MDFile {self.id}>"
  

class Page(Base):
  __tablename__ = 'pages'

  id: Mapped[int] = mapped_column(primary_key=True)
  title: Mapped[str] = mapped_column(sa.String(255), nullable=False)
  draft: Mapped[bool] = mapped_column(sa.Boolean, nullable=False)
  type: Mapped[str] = mapped_column(sa.String(10), nullable=False)
  relative_path: Mapped[str] = mapped_column(sa.String(255), nullable=False)

  blog_post: Mapped['BlogPost'] = relationship(back_populates='page')

  md_file_id: Mapped[int] = mapped_column(sa.ForeignKey('md_files.id'), nullable=True)
  md_file: Mapped['MDFile'] = relationship(back_populates='page')

  def __repr__(self):
    return f"<Page {self.id}>"


class BlogPost(Base):
  __tablename__ = 'blog_posts'

  id: Mapped[int] = mapped_column(primary_key=True)
  published: Mapped[datetime.datetime] = mapped_column(
    sa.DateTime(timezone=True), server_default=None, nullable=True
  )

  cover_photo_id: Mapped[int] = mapped_column(sa.ForeignKey('images.id'), nullable=True)
  cover_photo: Mapped['Image'] = relationship(foreign_keys=cover_photo_id)

  thumbnail_id: Mapped[int] = mapped_column(sa.ForeignKey('images.id'), nullable=False)
  thumbnail: Mapped['Image'] = relationship(foreign_keys=thumbnail_id)

  page_id: Mapped[int] = mapped_column(sa.ForeignKey('pages.id'))
  page: Mapped['Page'] = relationship(back_populates='blog_post')


  def __repr__(self):
    return f"<BlogPost {self.id}>"


class Image(Base):
  __tablename__ = 'images'

  id: Mapped[int] = mapped_column(primary_key=True)
  url: Mapped[str] = mapped_column(sa.String(255))

  attributes: Mapped[List["ImageAttribute"]] = relationship(back_populates="image")

  def get_attibute_value_for_key(self, key: str):
    try: 
      matches = list(filter(lambda attribute: attribute.key == key, self.attributes))
    except:
      raise KeyError(f'Unable to find attribute key {key} for {repr(self)}')
    
    return matches[0].value

  def __repr__(self):
    return f"<Image {self.id}>"
  

class ImageAttribute(Base): 
  __tablename__ = 'image_attributes'

  image_id: Mapped[int] = mapped_column(sa.ForeignKey('images.id'))
  image: Mapped['Image'] = relationship(back_populates="attributes")

  key: Mapped[str] = mapped_column(sa.String(55), nullable=False)
  value: Mapped[str] = mapped_column(sa.String(255))

  # @hybrid_property
  # def key(self):
  #   return self._key
  
  # @key.setter
  # def key(self, name: str):
  #   self._key = name

  # @hybrid_property
  # def value(self):
  #   return self._value
  
  # @key.setter
  # def value(self, value: str):
  #   self._value = value

  __table_args__ = (sa.PrimaryKeyConstraint("image_id", "key"),)

  def __repr__(self):
    return f"<ImageAttribute {self.key} for Image {self.image_id}>"
