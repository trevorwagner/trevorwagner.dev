from urllib.request import urlopen
import json
from os import path
from .get_photo_dimensions import get_photo_dimensions


def query_photo_details(photo_url):
    md_url = ''.join([str(path.dirname(photo_url)), '/md.json'])
    resp = urlopen(md_url).read()
    details = json.loads(resp)

    details['url'] = photo_url
    details['dimensions'] = get_photo_dimensions(photo_url)

    return details
