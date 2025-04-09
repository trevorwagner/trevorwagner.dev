import frontmatter as fm
import datetime, pathlib

from _static import get_file_mod_time
from src.inventory import BlogPost, Page, MDFile, Image, ImageAttribute, ImageVariant
from src.analysis.md_files import (
    get_page_relative_path,
    get_page_type,
)


def build_image_record(image_name, image_data):
    new_record = Image(name=image_name)

    if "author" in image_data:
        new_record.attributes.append(
            ImageAttribute(
                key="author_name", value=image_data["author"]["username"]
            )
        )
        if "profile" in image_data["author"]:
            new_record.attributes.append(
                ImageAttribute(
                    key="author_url", value=image_data["author"]["profile"]
                ),
            )
        if "source" in image_data:
            new_record.attributes.append(
                ImageAttribute(key="source_url", value=image_data["source"]),
            )

    if "description" in image_data:
        new_record.attributes.append(
            ImageAttribute(key="description", value=image_data["description"]),
        )
    for v_item in image_data["variants"]:
        new_record.variants.append(
            ImageVariant(
                url=v_item['url'],
                width=v_item["width"],
                height=v_item["height"],
                mime_type=v_item["mime-type"],
                length=v_item["length"],
            )
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
        alt_title=(
            md_file_metadata["altTitle"] if "altTitle" in md_file_metadata else None
        ),
        type=page_type,
        draft=md_file_metadata["draft"],
        relative_path=page_relative_path,
        md_file=md_file,
    )


def build_md_file_record(file_path: pathlib.Path, file_contents: str):
    new_record = MDFile(file_path=file_path, mod_time=get_file_mod_time(file_path))

    frontmatter = fm.loads(file_contents)

    new_record.page_metadata = frontmatter.metadata
    new_record.page_content = frontmatter.content

    return new_record
