from dataclasses import dataclass


@dataclass
class PhotoDimensions:
  w: int
  h: int


@dataclass
class PhotoDTO:
  url: str
  dimensions: PhotoDimensions
  details: dict[str, str]
