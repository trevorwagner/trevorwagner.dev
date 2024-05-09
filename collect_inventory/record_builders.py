import frontmatter as fm
import json, datetime, pathlib

from inventory_service.models import BlogPost, Page, MDFile, Image, ImageAttribute
from collect_inventory.analysis import (
    get_page_relative_path,
    get_page_type,
    get_photo_dimensions,
)


def build_image_record(url, photo_data):
    parsed_metadata = json.loads(photo_data)

    new_record = Image(url=url)

    if "author" in parsed_metadata:
        new_record.attributes.extend(
            [
                ImageAttribute(
                    key="author_name", value=parsed_metadata["author"]["username"]
                ),
                ImageAttribute(
                    key="author_url", value=parsed_metadata["author"]["profile"]
                ),
            ]
        )

    new_record.attributes.append(
        ImageAttribute(key="source_url", value=parsed_metadata["source"])
    )

    image_dimensions =  get_photo_dimensions(url)

    new_record.attributes.extend(
        [
            ImageAttribute(key="image_height", value=image_dimensions["w"]),
            ImageAttribute(key="image_width", value=image_dimensions["h"]),
        ]
    )

    return new_record


def build_blog_post_record(page_record: Page):
    md_file_metadata = page_record.md_file.page_metadata

    post_publication_date = datetime.datetime.fromisoformat(
        md_file_metadata["publishDate"]
    )

    new_record = BlogPost()
    new_record.published = post_publication_date

    new_record.page = page_record

    return new_record


def build_page_record(md_file: MDFile):

    md_file_metadata = md_file.page_metadata

    page_type = get_page_type(md_file.file_path)
    page_relative_path = get_page_relative_path(md_file.file_path, page_type)

    return Page(
        title=md_file_metadata["title"],
        type=page_type,
        draft=md_file_metadata["draft"],
        relative_path=page_relative_path,
        md_file=md_file,
    )


def build_md_file_record(file_path: pathlib.Path, file_contents: str):
    mod_time = file_path.stat().st_mtime

    new_record = MDFile(
        file_path=file_path, mod_time=datetime.datetime.fromtimestamp(mod_time)
    )

    frontmatter = fm.loads(file_contents)

    new_record.page_metadata = frontmatter.metadata
    new_record.page_content = frontmatter.content

    return new_record
