from sqlalchemy.orm import Session

from _static import list_page_files, list_post_files
from collect_inventory.builders.md_file_record_builder import build_md_file_record
from collect_inventory.builders.page_record_builder import build_page_record
from site_data_service import engine, init_db

if __name__ == '__main__':
  init_db()

  with Session(engine) as session:

    # Add brochure pages in any order.
    for file in list_page_files():
      md_file = build_md_file_record(file)

      with open(file) as f:
        page_record = build_page_record(file, f.read())
        page_record.md_file = md_file

        session.add(page_record)
        session.commit()

    # Add Blog posts, sorted in order of publicationDate.
    blog_posts = []

    for file in list_post_files():
      md_file = build_md_file_record(file)

      with open(file) as f:
        page_record = build_page_record(file, f.read())
        page_record.md_file = md_file

        blog_posts.append(page_record)

    blog_posts_sorted = sorted(blog_posts, key=lambda x: x.published)
    session.add_all(blog_posts_sorted)
    session.commit()