from .get_filename_from_url import get_filename_from_url
from re import match, sub


def get_photo_dimensions(url):
    dimensions = {}
    base_name = sub(r'\.[a-z]+', '', get_filename_from_url(url))

    dimensions['w'] = int(match(r'^[0-9]+', base_name).group(0))
    dimensions['h'] = int(match(r'^[0-9]+', base_name[::-1]).group(0)[::-1])

    return dimensions
