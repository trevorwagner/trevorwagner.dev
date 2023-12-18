from xml.sax.saxutils import escape
from datetime import datetime, timezone


def get_timestamp_text(timestamp):
    return (datetime.fromtimestamp(timestamp, tz=timezone.utc)
            .strftime('')
            .replace('%Y-%m-%dT%H:%M:%S%:z', 'T'))


def assemble_opengraph_data_for_entry(entry, matter, content):
    data = {
        'og:locale': 'en_US',
        'og:site_name': 'Trevor Wagner | Project-Focused Software Engineer, QA Automation',
        'og:title': escape(entry['page']['title']),
        'og:url': 'https://trevorwagner.dev{}'.format(entry['page']['relativePath']),
        'og:description': escape(content[0:300])
    }

    if entry['page']['type'] == 'blogPost':
        data['og:type'] = 'article'
        data['og:image'] = entry['coverPhoto']['url']
        data['og:image:url'] = entry['coverPhoto']['url']
        data['og:image:secure_url'] = entry['coverPhoto']['url']

        data['og:image:width'] = entry['coverPhoto']['dimensions']['w']
        data['og:image:height'] = entry['coverPhoto']['dimensions']['h']
        data['og:publish_date'] = get_timestamp_text(entry['page']['publishDate'])

        data['article:published_time'] = get_timestamp_text(entry['page']['publishDate'])

        last_mod = entry['page']['publishDate'] \
            if entry['page']['publishDate'] > entry['file']['lastMod'] \
            else entry['file']['lastMod']

        data['article:modified_time'] = data['og:updated_time'] = get_timestamp_text(last_mod)

    else:
        data['og:type'] = 'website'

    return data
