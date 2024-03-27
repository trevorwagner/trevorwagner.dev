from dataclasses import dataclass
from photo_info import PhotoDTO

from .page_dto import PageDTO


@dataclass
class BlogPostDTO(PageDTO):
  publish_date: int
  cover_photo: PhotoDTO
