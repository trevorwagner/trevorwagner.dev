import json

from sqlalchemy.orm import Session

from _static import list_page_files, list_post_files, get_file_contents, static_content
from src.analysis import get_metadata_for_image
from src.inventory import (
    engine,
    init_db,
    Page,
    MDFile,
    build_image_record,
    build_md_file_record,
    build_page_record,
    build_blog_post_record,
)


if __name__ == "__main__":
    init_db()

    with Session(engine) as session:

        # Add brochure pages in any order.
        for file in list_page_files():
            md_file = build_md_file_record(file, get_file_contents(file))
            page_record = build_page_record(md_file)
            page_record.type = (
                "custom" if page_record.relative_path == "/contact/" else "brochurePage"
            )

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

                photo_name = blog_post.page.md_file.page_metadata["coverPhoto"]

                image_metadata = get_metadata_for_image(
                    "https://static.trevorwagner.dev/images/image-details.php?n={}".format(
                        photo_name
                    )
                )

                blog_post.cover_photo = build_image_record(
                    photo_name, json.loads(image_metadata)
                )

            # Currently all blog posts need a thumbnail to be specified.
            # If I expect to support a default thumbnail, then I need to do extra work.
            # This should should alert me either to operator error or need for extra work.

            blog_posts.append(blog_post)

        posts_sorted_by_pubdate = sorted(blog_posts, key=lambda x: x.published)
        session.add_all(posts_sorted_by_pubdate)
        session.commit()

        blog_home = Page(
            title="Blog: Recent Posts",
            alt_title="Recent Posts",
            draft=False,
            type="custom",
            relative_path="/blog/",
            md_file=MDFile(
                file_path="{}/pages/blog.md".format(static_content),
                mod_time=posts_sorted_by_pubdate[-1].page.md_file.mod_time,
                _page_metadata=None,
                page_content=None,
            ),
        )

        session.add(blog_home)
        session.commit()
