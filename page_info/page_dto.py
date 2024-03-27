from dataclasses import dataclass
from md_file_dto import MDFileDTO


@dataclass
class PageDTO:
  md_file = MDFileDTO
  slug: str
  title: str
  content: str
  draft: bool
  relative_path: str


