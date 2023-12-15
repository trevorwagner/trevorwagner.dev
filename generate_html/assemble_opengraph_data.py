from xml.sax.saxutils import escape
from datetime import datetime, timezone


def get_timestamp_text(timestamp):
    return str(datetime.fromtimestamp(timestamp, tz=timezone.utc)).replace(' ', 'T')


def assemble_opengraph_data_for_entry(entry, matter, content):
    data = {
        'locale': 'en_US',
        'site_name': 'Trevor Wagner',
        'title': escape(entry['page']['title']),
        'url': 'https://trevorwagner.dev{}'.format(entry['page']['title']),
        'description': escape(content[0:300])
    }

    if entry['page']['type'] == 'blogPost':
        data['og:type'] = 'article'
        data['og:image'] = entry['coverPhoto']['url']
        data['og:image:url'] = entry['coverPhoto']['url']
        data['og:image:secure_url'] = entry['coverPhoto']['url']

        data['og:image:width'] = entry['coverPhoto']['dimensions']['w']
        data['og:image:height'] = entry['coverPhoto']['dimensions']['h']

        data['article:published_time'] = get_timestamp_text(entry['page']['publishDate'])

        last_mod = entry['page']['publishDate'] \
            if entry['page']['publishDate'] > entry['file']['lastMod'] \
            else entry['file']['lastMod']

        data['article:modified_time'] = data['og:updated_time'] = get_timestamp_text(last_mod)

    else:
        data['og:type'] = 'website'

    return data
