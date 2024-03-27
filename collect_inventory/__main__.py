from sqlalchemy.orm import Session

from _static import list_page_files
from collect_inventory.builders.md_file_record_builder import build_md_file_record
from collect_inventory.builders.page_record_builder import build_page_record
from site_data_service import engine, init_db

if __name__ == '__main__':
  init_db()

  with Session(engine) as session:

    for file in list_page_files():
      md_file = build_md_file_record(file)

      with open(file) as f:
        page_record = build_page_record(file, f.read())
        page_record.md_file = md_file

        session.add(page_record)
        session.commit()
