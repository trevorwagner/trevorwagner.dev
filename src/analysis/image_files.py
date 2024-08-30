import os

from pathlib import Path
from re import match, sub
from urllib.parse import urlparse

from src.http_io import http_get


def get_filename_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    return Path(path).name


def get_photo_dimensions(url):
    dimensions = {}
    base_name = sub(r"\.[a-z]+", "", get_filename_from_url(url))

    dimensions["w"] = int(match(r"^[0-9]+", base_name).group(0))
    dimensions["h"] = int(match(r"^[0-9]+", base_name[::-1]).group(0)[::-1])

    return dimensions


def get_metadata_for_image(image_url):
    md_url = "".join([str(os.path.dirname(image_url)), "/md.json"])

    image_data = http_get(md_url).read().decode()

    return image_data


def get_headers_for_image(image_url):
    header_data = http_get(image_url).headers
    return header_data
