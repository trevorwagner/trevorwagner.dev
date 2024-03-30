from datetime import datetime

import frontmatter

from collect_inventory.analysis.get_page_type import get_page_type
from collect_inventory.analysis.get_page_relative_path import get_page_relative_path
from site_data_service import Page


def build_page_record(file_path, file_content):
  file_front_matter = frontmatter.parse(file_content)

  page_title = file_front_matter[0]['title']
  page_type = get_page_type(file_path)
  page_draft_status = file_front_matter[0]['draft']
  if 'publishDate' in file_front_matter[0].keys():
    page_publication_date = datetime.fromisoformat(file_front_matter[0]['publishDate'])
  else:
    page_publication_date = None

  page_relative_path = get_page_relative_path(file_path, page_type)
  page_content = file_front_matter[1]

  return Page(
    title=page_title,
    type=page_type,
    draft=page_draft_status,
    published=page_publication_date,
    relative_path=page_relative_path,
    content=page_content
  )
