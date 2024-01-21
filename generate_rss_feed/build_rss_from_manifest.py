from datetime import datetime
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

build_time = datetime.now(tz=ZoneInfo('America/Chicago'))


def timestamp_rfc_822(time):
    return time.strftime("%a, %d %b %Y %H:%M:%S %z" )


metadata = {
    "title": 'trevorwagner.dev - Blog',
    "description": 'RSS Feed for new blog posts on trevorwagner.dev',
    "language": 'en-us',
    "link": 'https://trevorwagner.dev/blog/',
    "lastBuildDate": timestamp_rfc_822(build_time),
    "copyright": '{} Upstream Consulting LLC. All rights reserved.'.format(build_time.strftime("%Y"))
}


def build_rss_from_inventory(manifest):
    rss = ''.join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '\n<rss version="2.0">'
    ])

    channel = ''.join([
        '\n\n<channel>',
        '\n\t<title>{}</title>'.format(escape(metadata["title"])),
        '\n\t<link>{}</link>'.format(metadata["link"]),
        '\n\t<description>{}</description>'.format(escape(metadata["description"])),
        '\n\t<lastBuildDate>{}</lastBuildDate>'.format(metadata["lastBuildDate"]),
        '\n\t<language>{}</language>'.format(metadata["language"]),
        '\n\t<copyright>{}</copyright>'.format(escape(metadata["copyright"])),
    ])

    sorted_blog_posts = sorted(
        [e for e in manifest['site'] if e['page']['type'] == 'blogPost'],
        key=lambda i: i["page"]['publishDate'],
        reverse=True
    )
    for post in sorted_blog_posts:

        new_item = ''.join([
            '\n\t<item>',
            '\n\t\t<title>{}</title>'.format(post["page"]["title"]),
            '\n\t\t<link>https://trevorwagner.dev{}</link>'.format(escape(post["page"]["relativePath"])),
            '\n\t\t<pubDate>{}</pubDate>'.format(timestamp_rfc_822(datetime.fromtimestamp(
                post["page"]['publishDate'], tz=ZoneInfo('America/Chicago'))
            )),
            # TODO: Add summaries to each blog post MD, to use for Description here.
            # TODO: Add summary element to manifest generation script.
            # '\n\t\t<description>{}</description>.format()'.format(escape(post["description"])),
            '\n\t</item>'
        ])

        channel = ''.join([channel, new_item])

    channel = ''.join([channel, '\n\n</channel>'])

    rss = ''.join([rss, channel])
    rss = ''.join([rss, '\n\n</rss>'])

    return rss
