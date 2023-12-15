from urllib.parse import urlparse
from pathlib import Path


def get_filename_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    return Path(path).name
