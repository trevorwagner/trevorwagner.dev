from dataclasses import dataclass
from typing import Any


@dataclass
class MDFileDTO:
  path: str
  last_mod: int
  front_matter: dict[str, Any]
  md_content: str
