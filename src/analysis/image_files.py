import os

from pathlib import Path
from re import match, sub
from urllib.parse import urlparse

from src.http_io import http_get


def get_filename_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path

    return Path(path).name


def get_metadata_for_image(image_url):
    image_data = http_get(image_url)

    return image_data
