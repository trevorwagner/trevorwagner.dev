from pathlib import Path
from os import path
from re import match, sub
from urllib.parse import urlparse

from collect_inventory.http_io import get_remote_data


def get_page_relative_path(file_path, page_type):
    slug = Path(file_path).stem

    # TODO: Explore updating to match statement once I upgrade to python >= 3.10.
    # TODO: Rewrite this so that it only takes one argument (file_path).
    if page_type == "blogPost":
        return f"/blog/posts/{slug}/"
    elif slug == "index":
        return "/"
    else:
        return "/{}/".format(slug)


def get_page_type(file_path):
    f = ""
    page_type = ""

    try:
        f = match(r".*/_static/(.*)/", str(file_path)).group(1)
    except:
        f = "/"

    if f == "posts":
        page_type = "blogPost"
    elif f == "pages" or f == '/':
        page_type = "brochurePage"
    else:
        page_type = "custom"

    return page_type


def get_metadata_for_image(image_url):
    md_url = "".join([str(path.dirname(image_url)), "/md.json"])

    image_data = get_remote_data(md_url)
    
    return image_data


def get_filename_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    return Path(path).name


def get_photo_dimensions(url):
    dimensions = {}
    base_name = sub(r'\.[a-z]+', '', get_filename_from_url(url))

    dimensions['w'] = int(match(r'^[0-9]+', base_name).group(0))
    dimensions['h'] = int(match(r'^[0-9]+', base_name[::-1]).group(0)[::-1])

    return dimensions