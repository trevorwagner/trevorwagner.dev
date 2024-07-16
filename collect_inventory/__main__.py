from sqlalchemy.orm import Session

from _static import list_page_files, list_post_files, get_file_contents
from collect_inventory.analysis.image_files import (
    get_metadata_for_image,
    get_headers_for_image,
)
from collect_inventory.record_builders import (
    build_image_record,
    build_md_file_record,
    build_page_record,
    build_blog_post_record,
)
from inventory_service import engine, init_db, Page, MDFile


if __name__ == "__main__":
    init_db()

    with Session(engine) as session:

        # Add brochure pages in any order.
        for file in list_page_files():
            md_file = build_md_file_record(file, get_file_contents(file))
            page_record = build_page_record(md_file)
            if page_record.relative_path == '/contact/':
                page_record.type="custom"

            session.add(page_record)
            session.commit()

        # Add Blog posts, sorted in order of publicationDate.
        blog_posts = []

        for file in list_post_files():
            md_file = build_md_file_record(file, get_file_contents(file))
            page_record = build_page_record(md_file)
            page_record.type = "blogPost"

            blog_post = build_blog_post_record(page_record)

            # I anticipate that some blog posts may not have cover photos.
            # TODO: This is not catching where coverPhoto is set but has no contents.
            if "coverPhoto" in blog_post.page.md_file.page_metadata:
                cover_url = blog_post.page.md_file.page_metadata["coverPhoto"]

                cover_metadata = get_metadata_for_image(cover_url)
                cover_headers = get_headers_for_image(cover_url)
                blog_post.cover_photo = build_image_record(
                    cover_url, cover_metadata, cover_headers
                )

            # Currently all blog posts need a thumbnail to be specified.
            # If I expect to support a default thumbnail, then I need to do extra work.
            # This should should alert me either to operator error or need for extra work.
            try:
                thumb_url = blog_post.page.md_file.page_metadata["thumbnail"]
                thumb_metadata = get_metadata_for_image(thumb_url)
                blog_post.thumbnail = build_image_record(
                    thumb_url, thumb_metadata, None
                )
            except KeyError:
                raise KeyError(
                    f'No thumbnail was provided for the post "{blog_post.page.title}" (via {blog_post.page.md_file.file_path})'
                )

            blog_posts.append(blog_post)

        posts_sorted_by_pubdate = sorted(blog_posts, key=lambda x: x.published)
        session.add_all(posts_sorted_by_pubdate)
        session.commit()

        latest_blog_post = (
            session.query(Page)
            .join(MDFile)
            .filter(Page.type == "blogPost")
            .order_by(MDFile.mod_time.desc())
            .first()
        )

        blog_home = Page(
            title="Recent Posts",
            draft=False,
            type="custom",
            relative_path="/blog/",
            md_file=None,
        )

        session.add(blog_home)
        session.commit()
